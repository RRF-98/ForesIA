package com.forensia.model;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Data

@Builder

@NoArgsConstructor

@AllArgsConstructor

@Entity

@Table(name = "Data")

public class Analysis {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "user",
            unique = true,
            nullable = false)
    private String username;

    @Enumerated(EnumType.STRING)
    @Column(name = "role",
            nullable = false,
            length = 20) // Cria a coluna para falar se é usuario ou adm
    @Builder.Default
    private String role = "User";

    @Column(name = "probability",
            precision = 5,
            scale = 2) // Cria a coluna da chance de ser IA
    private Double Probability;

    @Enumerated(EnumType.STRING)
    @Column(name = "file_type",
            nullable = false,
            length = 20) // Cria a coluna para dizer o tipo de arquivos
    private String File_Type;

    @CreationTimestamp
    @Column(name = "created_at",
            updatable = false) // Cria a coluna de horario
    private LocalDateTime Created_at;
}
