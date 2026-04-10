package com.forensia.dto.request;


import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@NoArgsConstructor
@AllArgsConstructor
@Data
public class TextRequest {
    @NotBlank(message = "O texto não pode ser vazio!!!")
    @Size(min = 5,
    message = "O texto deve conter no minimo 5 caracteres!!!")
    private String Text;



}
