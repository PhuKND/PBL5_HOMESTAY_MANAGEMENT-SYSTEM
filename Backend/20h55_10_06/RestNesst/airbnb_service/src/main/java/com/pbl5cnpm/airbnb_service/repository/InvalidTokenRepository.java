package com.pbl5cnpm.airbnb_service.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.pbl5cnpm.airbnb_service.entity.InvalidTokenEntity;

@Repository
public interface InvalidTokenRepository extends MongoRepository<InvalidTokenEntity, String> {
    
}
