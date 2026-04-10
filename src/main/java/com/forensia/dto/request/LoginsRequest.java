package com.forensia.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoginsRequest {
    @NotBlank(message = "O nome é obrigatorio")
    @Size(min = 5, max = 20,
            message = "O nome dever ter entre 5 a 20 caracteres")
    private String Username;


    @NotBlank(message = "A senha é obrigatorio")
    @Pattern(regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[?=.*\\d]).{8,}$", message = "A senha deve ter no minimo 8 caracteres, contendo letras minusculas, maiusculas e numeros  ")
    @Size(min = 5, max = 255,
            message = "O nome dever ter entre 5 a 255 caracteres")
    private String Password_user;
}
