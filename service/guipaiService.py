import google.generativeai as genai
import json

from statistics import mean

def calculate_score(percentual_responses):
  int_list = list(map(int, percentual_responses))
  result = mean(int_list)
  return result

def toMarkdown(text):
    try:
        cleaned_data = text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_data)
    except: 
        model = genai.GenerativeModel('gemini-pro')
        context = f"Voce está sendo executado no seguinte script def toMarkdown(text):\ntry:\ncleaned_data = text.replace(\"```json\", "").replace(\"```\", "").strip()\nreturn json.loads(cleaned_data)\nexcept:\nmodel = genai.GenerativeModel('gemini-pro')\ncontext = \"contexto para evitar erro no json.loads\"\nresponse = model.generate_content().text\nreturn json.loads(response). o que eu quero fazer é que o {text} seja adicionado em json loads, então faça os ajustes necessarios em text para ajeitar isso e retorne apenas text, pois perceba que no script o retorno desse prompt vai ser colocado dentro de json.loads"
        response = model.generate_content(context).text
        return json.loads(response)

def callingGuipAICorrecao(body):
    try:
        GOOGLE_API_KEY = 'AIzaSyA7bjbkIagAXX2CBHBtibw8c4Gcfm0sQtw'
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        context = "Você é um professor de programação e está aplicando uma prova. Você precisa responder se a resposta dos seus alunos estão certas ou erradas."

        student_responses = [model.generate_content(f"{context}\nPara essa pergunta: {item['questao']}, você espera que a resposta do aluno esteja dentro desse contexto: {item['contexto']}, corrija se para essa resposta: {item['resposta']}, se o que o aluno disse está no contexto informado e retorne um feedback informando o motivo de estar certo ou errado, correlacionando com temas. Retorne essa feedback como um json no seguinte padrão: [\"nota\": nota_da_questao_inteiro, \"pergunta\": \"pergunta\", \"resposta\": \"resposta\", \"contexto\": \"contexto\", \"feedback_ia\": \"feedback_ia\"], seja bem rigido quanto a nota, se o aluno não explicou como o pedido no contexto, retire alguns pontos da nota. (APENAS RETORNE A PORCENTAGEM SEM O CARACTER '%' dentro do json e ele deveria ser um inteiro)").text for item in body['items']]
        
        student_responses = [toMarkdown(student_responses[i]) for i in range(len(student_responses))]

        percentual_responses = [student_responses[i]["nota"] for i in range(len(student_responses))]

        score = calculate_score(percentual_responses)

        response = {
            "percentual_responses": score,
            "student_responses": student_responses
        }
        return 200, response
    except Exception as e:
        return 500, f"Error: {e}"

def callingGuipAIRecorrecao(body):
    try:
        GOOGLE_API_KEY = 'AIzaSyA7bjbkIagAXX2CBHBtibw8c4Gcfm0sQtw'
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        context = "Você é um professor de programação e corrigiu uma questão da seguinte maneira:"

        student_responses = body["student_responses"]

        student_responses = [model.generate_content(f"{context}\nPara a pergunta: {item["pergunta"]}, o aluno respondeu: {item["resposta"]}. Em sua primeira correção, voce disse o seguinte sobre a resposta do aluno: {item["feedback_ia"]} e deu a seguinte nota: {item["nota"]}, essa nota está em percentual de (0 a 100). Essa correção e nota foi baseado no seguinte contexto: {item["contexto"]} que voce mesmo tinha definido para que a resposta estivesse dentro, ou seja, a resposta tinha que está dentro desse contexto. O coordenador recebeu uma reclamação do aluno e questionou sua correção dando o seguinte comentario: {item["feedback_coordenador"]}. Seu trabalho é rever isso e levar em consideração o comentario do coordenador alterando ou não a nota. E adicionando ao json: {item} o campo \"recorreção\": \"sua_recorrecao\" e alterando o score. Retornando o json alterado, apenas o json. lembresse de colocar o json com aspas dupla nas chaves e valores quando precisar.").text for item in student_responses]

        student_responses = [toMarkdown(student_responses[i]) for i in range(len(student_responses))]

        percentual_responses = [student_responses[i]["nota"] for i in range(len(student_responses))]

        score = calculate_score(percentual_responses)

        response = {
            "percentual_responses": score,
            "student_responses": student_responses
        }
        return 200, response
    except Exception as e:
        return 500, f"Error accessing the bucket {e}"