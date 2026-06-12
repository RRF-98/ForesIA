package com.forensia.repository;

import com.forensia.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByUsername(String username);

    Optional<User> findByEmail_user(String email);

    // FIX: era existByUsername (typo) — Spring Data requer prefixo "existsBy"
    boolean existsByUsername(String username);

    // FIX: era existByEmail_user (typo)
    boolean existsByEmail_user(String email);

    // REMOVIDO: findByPassword_user e existByPassword_user — anti-pattern,
    // nunca buscar usuario por senha em texto plano
}
