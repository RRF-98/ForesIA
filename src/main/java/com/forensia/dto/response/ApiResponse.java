package com.forensia.dto.response;


import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.Timer;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Data
public class ApiResponse<T> {

    private boolean sucess;

    private T data;

    private String error;

    private LocalDateTime timestamp;

    public static <T> ApiResponse<T> ok(T data){
        return ApiResponse.<T>builder()
                .sucess(true)
                .data(data)
                .error(null)
                .timestamp(LocalDateTime.now())
                .build();
    }
    public static <T> ApiResponse<T> error(String message){
        return ApiResponse.<T>builder()
                .sucess(false)
                .data(null)
                .error(message)
                .timestamp(LocalDateTime.now())
                .build();
    }


}
