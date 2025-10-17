package com.pbl5cnpm.airbnb_service.entity;

import java.util.Date;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.FieldDefaults;

@Document(collection = "InvalidToken")
@FieldDefaults(level = AccessLevel.PRIVATE)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class InvalidTokenEntity {
    @Id
    String id;
    Date expired;
}
