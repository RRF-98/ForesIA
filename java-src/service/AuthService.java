package com.forensia.service;

import com.forensia.dto.request.LoginsRequest;
import com.forensia.dto.request.RegisterRequest;
import com.forensia.dto.response.ApiResponse;
import com.forensia.model.User;
import com.forensia.repository.UserRepository;
import com.forensia.security.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final AuthenticationManager authenticationManager;

    public ApiResponse<?> register(RegisterRequest request) {
        if (userRepository.existsByUsername(request.getUsername())) {
            return ApiResponse.error("Nome de usuario ja esta em uso");
        }
        if (userRepository.existsByEmail_user(request.getEmail_user())) {
            return ApiResponse.error("Email ja esta em uso");
        }

        User user = new User();
        user.setUsername(request.getUsername());
        user.setEmail_user(request.getEmail_user());
        user.setPassword_user(passwordEncoder.encode(request.getPassword_user()));
        user.setRole("USER");

        userRepository.save(user);
        return ApiResponse.ok(Map.of("message", "Usuario registrado com sucesso"));
    }

    public ApiResponse<?> login(LoginsRequest request) {
        try {
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            request.getUsername(),
                            request.getPassword_user()
                    )
            );
        } catch (BadCredentialsException e) {
            return ApiResponse.error("Credenciais invalidas");
        }

        String token = jwtUtil.generateToken(request.getUsername());
        return ApiResponse.ok(Map.of(
                "token", token,
                "type", "Bearer",
                "username", request.getUsername()
        ));
    }
}
