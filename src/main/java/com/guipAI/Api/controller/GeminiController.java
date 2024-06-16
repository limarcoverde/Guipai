package com.guipAI.Api.controller;

import com.guipAI.Api.model.PromptResponse;
import com.guipAI.Api.service.PromptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class GeminiController {

    @Autowired
    private PromptService promptService;

    @PostMapping("/prompt")
    public ResponseEntity<?> getResponse(
            @RequestHeader(value = "Authorization") String authHeader,
            @RequestBody Map<String, String> body) throws IOException {
        String response = promptService.getResponseFromGemini(body);
        return ResponseEntity.ok(response);
    }
}