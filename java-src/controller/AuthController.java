package com.forensia.controller;

import com.forensia.dto.request.LoginsRequest;
import com.forensia.dto.request.RegisterRequest;
import com.forensia.dto.response.ApiResponse;
import com.forensia.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<?>> register(@Valid @RequestBody RegisterRequest request) {
        return ResponseEntity.ok(authService.register(request));
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<?>> login(@Valid @RequestBody LoginsRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }
}
