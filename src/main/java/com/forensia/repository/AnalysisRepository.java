package com.forensia.repository;

import com.forensia.model.Analysis;
import com.forensia.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;



@Repository
public interface AnalysisRepository extends JpaRepository<Analysis, Long> {

    List<Analysis> findByUsername (String username);

    long countByUsername (String username);

    List<Analysis> findByProbability (Double Probability);

    List<Analysis> findByFile_Type (String File_Type);

    List<Analysis> findByUsername_File_Type (String username, String File_Type);


}
