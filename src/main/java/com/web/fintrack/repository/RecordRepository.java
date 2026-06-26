package com.web.fintrack.repository;


import com.web.fintrack.domain.enums.TransactionCategory;
import com.web.fintrack.domain.enums.TransactionType;

import java.util.List;
import java.util.Optional;

public interface RecordRepository<Entity, EntityType> {

    Entity save(Entity entity);

    Optional<Entity> findById(EntityType id);
    List<Entity> findByType(TransactionType transactionType);
    List<Entity> findByCategory(TransactionCategory transactionCategory);

    List<Entity> findAll();

    void deleteById(EntityType id);

    boolean existsById(EntityType id);
}
