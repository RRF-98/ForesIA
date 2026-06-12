package com.forensia.controller;

import com.forensia.dto.request.TextRequest;
import com.forensia.dto.response.AnalysisResult;
import com.forensia.dto.response.ApiResponse;
import com.forensia.service.AnalysisService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/analysis")
@RequiredArgsConstructor
public class AnalysisController {

    private final AnalysisService analysisService;

    /**
     * POST /api/v1/analysis/text
     * Body: { "text": "conteudo a analisar" }
     * Header: Authorization: Bearer <jwt>
     */
    @PostMapping("/text")
    public ResponseEntity<ApiResponse<AnalysisResult>> analyzeText(
            @Valid @RequestBody TextRequest request,
            Authentication authentication) {
        return ResponseEntity.ok(
                analysisService.analyzeText(authentication.getName(), request)
        );
    }
}
