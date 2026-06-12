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
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "username", unique = true, nullable = false, length = 50)
    private String Username;

    // FIX: removido @Enumerated — role é String, não Enum
    @Column(name = "role", nullable = false, length = 20)
    @Builder.Default
    private String role = "User";

    @Column(name = "email_user", unique = true, nullable = false, length = 100)
    private String Email_user;

    @Column(name = "password_user", nullable = false, length = 255)
    private String Password_user;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime Created_at;
    // FIX: removido import javax.swing.* (não usado)
}
