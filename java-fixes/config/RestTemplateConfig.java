package com.forensia.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

// INSTRUCAO: deletar o arquivo original RestTemplate.java (conflita com Spring RestTemplate)
// Este arquivo substitui com nome correto RestTemplateConfig.java
@Configuration
public class RestTemplateConfig {

    @Value("${ai-engine.url}")
    private String aiEngineUrl;

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean("aiEngineBaseUrl")
    public String aiEngineBaseUrl() {
        return aiEngineUrl;
    }
}
