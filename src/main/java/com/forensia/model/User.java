package com.forensia.model;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import javax.swing.*;
import java.time.LocalDateTime;
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity

@Table (name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) //Cria a coluna ID
    private Long id;

    @Column(name = "username",
        unique = true,
        nullable = false,
        length = 50) // Cria a coluna nome do usuario
    private String Username;

    @Enumerated(EnumType.STRING)
    @Column(name = "role",
            nullable = false,
            length = 20) // Cria a coluna para falar se é usuario ou adm
    @Builder.Default
    private String role = "User";

    @Column(name = "email_user",
        unique = true,
        nullable = false,
        length = 100) // Cria a coluna do email do usuario
    private String Email_user;

    @Column(name = "password_user",
        nullable = false,
        length = 255) // Cria a coluna da senha do usuario
    private String Password_user;

    @CreationTimestamp
    @Column(name = "created_at",
        updatable = false) // Cria a coluna de horario
    private LocalDateTime Created_at;
}
