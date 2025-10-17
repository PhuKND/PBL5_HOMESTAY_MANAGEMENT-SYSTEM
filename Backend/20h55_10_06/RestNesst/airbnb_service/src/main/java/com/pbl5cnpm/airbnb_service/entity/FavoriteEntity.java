package com.pbl5cnpm.airbnb_service.entity;

import java.time.LocalDateTime;

import jakarta.persistence.EmbeddedId;
import jakarta.persistence.Entity;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.MapsId;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.FieldDefaults;

@Getter
@Setter
@Builder
@Entity
@FieldDefaults(level = AccessLevel.PRIVATE)
@Table(name = "favorites")
@NoArgsConstructor
@AllArgsConstructor
public class FavoriteEntity {
    @EmbeddedId
    FavoriteKey id = new FavoriteKey();

    @ManyToOne
    @MapsId("userId")
    @JoinColumn(name = "user_id")
    UserEntity user;

    @ManyToOne
    @MapsId("listingId")
    @JoinColumn(name = "listing_id")
    ListingEntity listing;

    LocalDateTime createdAt;
    Boolean deteted;
    
}
