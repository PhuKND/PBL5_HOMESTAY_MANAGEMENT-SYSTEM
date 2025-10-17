package com.pbl5cnpm.airbnb_service.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.pbl5cnpm.airbnb_service.entity.FavoriteEntity;
import com.pbl5cnpm.airbnb_service.entity.FavoriteKey;

@Repository
public interface FavoriteRepository extends JpaRepository<FavoriteEntity, FavoriteKey> {
    
}
