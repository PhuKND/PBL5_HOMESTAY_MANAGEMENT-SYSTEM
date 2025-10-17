package com.pbl5cnpm.airbnb_service.service;

import org.springframework.stereotype.Service;

import com.pbl5cnpm.airbnb_service.entity.RoleEntity;
import com.pbl5cnpm.airbnb_service.repository.RoleRepository;

@Service

public class RoleService {
    private final RoleRepository repository;
    public RoleService(RoleRepository  repository){
        this.repository = repository;
    }
    public RoleEntity handleCreateRole(String roleName){
        RoleEntity role = RoleEntity.builder().roleName(roleName).build();
        return this.repository.save(role);
    }
}
