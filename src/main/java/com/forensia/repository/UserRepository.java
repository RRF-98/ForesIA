package com.forensia.repository;

import com.forensia.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;


public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByUsername(String Username); //Procura o nome do usuario no banco de dados

    Optional<User> findByEmail_user(String Email_user); //Procura o nome do Email_user no banco de dados

    Optional<User> findByPassword_user(String Password_user); //Procura o nome do Password_user no banco de dados

    boolean existByUsername (String Username); //Verifica se o nome de usuario no banco de dados

    boolean existByEmail_user(String Email_user); //Verifica se o nome de Email_user no banco de dados

    boolean existByPassword_user(String Password_user); //Verifica se o nome de Password_user no banco de dados
}
