package com.pbl5cnpm.airbnb_service.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.pbl5cnpm.airbnb_service.entity.CountriesEntity;

@Repository
public interface CountriesRepository extends JpaRepository<CountriesEntity, Long> {
    Optional<CountriesEntity> findByName(String name);
}
