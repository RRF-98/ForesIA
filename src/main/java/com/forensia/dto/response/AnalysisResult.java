package com.forensia.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Data
public class AnalysisResult {

    private Double Probability;

    private String Classification;

    private String File_Type;

    private String Warning;

    private LocalDateTime Created_at;
}
