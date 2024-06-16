package com.guipAI.Api.service;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.JsonNode;
import java.io.IOException;

import java.util.Map;

@Service
public class PromptService {

    private final RestTemplate restTemplate;

    public PromptService(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder.build();
    }

    public String getResponseFromGemini(Map<String, String> body) throws IOException {
        String questao = body.get("questao");
        String respostaAluno = body.get("resposta_aluno");
        String respostaProfessor = body.get("resposta_professor");

        String question = getCorrecao(questao, respostaProfessor, respostaAluno);

        String geminiApiKey = "AIzaSyA7bjbkIagAXX2CBHBtibw8c4Gcfm0sQtw";
        String API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=%s";
        String apiUrl = String.format(API_URL_TEMPLATE, geminiApiKey);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");

        ObjectMapper objectMapper = new ObjectMapper();
        ObjectNode contentNode = objectMapper.createObjectNode();
        ObjectNode partsNode = objectMapper.createObjectNode();
        partsNode.put("text", question);
        contentNode.set("parts", objectMapper.createArrayNode().add(partsNode));
        ObjectNode requestBodyNode = objectMapper.createObjectNode();
        requestBodyNode.set("contents", objectMapper.createArrayNode().add(contentNode));

        String requestBody;
        try {
            requestBody = objectMapper.writeValueAsString(requestBodyNode);
        } catch (Exception e) {
            throw new RuntimeException("Failed to construct JSON request body", e);
        }

        HttpEntity<String> request = new HttpEntity<>(requestBody, headers);

        ResponseEntity<String> response = restTemplate.exchange(apiUrl, HttpMethod.POST, request, String.class);

        return adjustJson(response.getBody());
    }

    private static String getCorrecao(String questao, String respostaProfessor, String respostaAluno) {
        String context = "Você é um professor de programação e está aplicando uma prova. Você precisa responder se a resposta dos seus alunos estão certas ou erradas.";

        return String.format("%s\nPara essa pergunta: %s, você espera que a resposta do aluno esteja dentro desse contexto: %s, corrija se para essa resposta: %s, se o que o aluno disse está no contexto informado e retorne um feedback informando o motivo de estar certo ou errado, correlacionando com temas. Retorne esse feedback como um json no seguinte padrão: [\"nota\": nota_da_questao_inteiro, \"pergunta\": \"pergunta\", \"resposta\": \"resposta\", \"contexto\": \"contexto\", \"feedback_ia\": \"feedback_ia\"], seja bem rígido quanto a nota, se o aluno não explicou como o pedido no contexto, retire alguns pontos da nota. (APENAS RETORNE A PORCENTAGEM SEM O CARACTER '%%' dentro do json e ele deveria ser um inteiro)",
                context, questao, respostaProfessor, respostaAluno);
    }

    public static String adjustJson(String inputJson) throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();
        JsonNode rootNode = objectMapper.readTree(inputJson);

        String text = rootNode.at("/candidates/0/content/parts/0/text").asText();

        String cleanedText = text.replaceAll("```json\\n|\\n```", "").trim();

        if (cleanedText.startsWith("[") && cleanedText.endsWith("]")) {
            cleanedText = cleanedText.substring(1, cleanedText.length() - 1).trim();
        }

        JsonNode extractedNode = objectMapper.readTree("{" + cleanedText + "}");

        ObjectNode adjustedNode = objectMapper.createObjectNode();

        adjustedNode.set("nota", extractedNode.get("nota"));
        adjustedNode.set("pergunta", extractedNode.get("pergunta"));
        adjustedNode.set("resposta", extractedNode.get("resposta"));
        adjustedNode.set("contexto", extractedNode.get("contexto"));
        adjustedNode.set("feedback_ia", extractedNode.get("feedback_ia"));

        return objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(adjustedNode);
    }
}
