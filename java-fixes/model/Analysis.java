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
@Table(name = "analyses")
public class Analysis {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // FIX: removido unique=true — usuario pode ter multiplas analyses
    @Column(name = "username", nullable = false)
    private String username;

    // FIX: removido @Enumerated — role é String, não Enum
    @Column(name = "role", nullable = false, length = 20)
    @Builder.Default
    private String role = "User";

    @Column(name = "probability", precision = 5, scale = 2)
    private Double Probability;

    // FIX: removido @Enumerated — File_Type é String, não Enum
    @Column(name = "file_type", nullable = false, length = 20)
    private String File_Type;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime Created_at;
}
