package com.pbl5cnpm.airbnb_service.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.pbl5cnpm.airbnb_service.dto.Request.FavoriteRequest;
import com.pbl5cnpm.airbnb_service.entity.FavoriteEntity;
import com.pbl5cnpm.airbnb_service.entity.FavoriteKey;
import com.pbl5cnpm.airbnb_service.exception.AppException;
import com.pbl5cnpm.airbnb_service.exception.ErrorCode;
import com.pbl5cnpm.airbnb_service.repository.FavoriteRepository;
import com.pbl5cnpm.airbnb_service.repository.ListingsRepository;
import com.pbl5cnpm.airbnb_service.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
@Transactional
public class FavoriteService {
    private final FavoriteRepository favoriteRepository;
    private final UserRepository userRepository;
    private final ListingsRepository listingsRepository;

    public void addFavorite( Long listingId, String username) {
        var userOpt = userRepository.findByUsername(username);
        var listingOpt = listingsRepository.findById(listingId);
        
        if (userOpt.isEmpty() || listingOpt.isEmpty()) {
            throw new AppException(ErrorCode.INVALID);
        }
        var userId = userOpt.get().getId();
        var favoriteKey = new FavoriteKey(userId, listingId);
        var favorite = FavoriteEntity.builder()
                .id(favoriteKey)
                .user(userOpt.get())
                .listing(listingOpt.get())
                .createdAt(java.time.LocalDateTime.now())
                .deteted(false)
                .build();

        favoriteRepository.save(favorite);
    }
    public void deleteFavorite(Long listingId, String username) {
        var user = userRepository.findByUsername(username)
                .orElseThrow(() -> new AppException(ErrorCode.USER_NOT_EXISTED));
        var listing = listingsRepository.findById(listingId)
                .orElseThrow(() -> new AppException(ErrorCode.INVALID));
    
        var favoriteKey = new FavoriteKey(user.getId(), listingId);
        var favorite = favoriteRepository.findById(favoriteKey)
                .orElseThrow(() -> new AppException(ErrorCode.FAVORITE_NOT_EXISTED));
    
        favorite.setDeteted(true);
        favoriteRepository.save(favorite); // update
    }
    
}
