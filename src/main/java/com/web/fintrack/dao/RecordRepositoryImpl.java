package com.web.fintrack.dao;

import com.web.fintrack.domain.enums.TransactionCategory;
import com.web.fintrack.domain.enums.TransactionType;
import com.web.fintrack.domain.model.Record;
import com.web.fintrack.repository.RecordRepository;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.EntityTransaction;
import jakarta.persistence.Persistence;
import jakarta.persistence.TypedQuery;

import java.util.List;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Function;

@ApplicationScoped
public class RecordRepositoryImpl implements RecordRepository<Record, String> {

    private EntityManagerFactory emf;

    @PostConstruct
    public void init() {
        emf = Persistence.createEntityManagerFactory("fintrack-pu");
    }

    @PreDestroy
    public void cleanup() {
        if (emf != null && emf.isOpen()) {
            emf.close();
        }
    }

    @Override
    public Record save(Record record) {
        return executeInTransaction(em -> em.merge(record));
    }

    @Override
    public Optional<Record> findById(String id) {
        return execute(em -> Optional.ofNullable(em.find(Record.class, id)));
    }

    @Override
    public List<Record> findByType(TransactionType transactionType) {
        return execute(em -> {
            TypedQuery<Record> query = em.createQuery(
                    "SELECT r FROM Record r WHERE r.transactionType = :type", Record.class);
            query.setParameter("type", transactionType);
            return query.getResultList();
        });
    }

    @Override
    public List<Record> findByCategory(TransactionCategory transactionCategory) {
        return execute(em -> {
            TypedQuery<Record> query = em.createQuery(
                    "SELECT r FROM Record r WHERE r.transactionCategory = :category", Record.class);
            query.setParameter("category", transactionCategory);
            return query.getResultList();
        });
    }

    @Override
    public List<Record> findAll() {
        return execute(em -> em.createQuery("SELECT r FROM Record r", Record.class).getResultList());
    }

    @Override
    public void deleteById(String id) {
        executeInTransactionVoid(em -> {
            Record record = em.find(Record.class, id);
            if (record != null) {
                em.remove(record);
            }
        });
    }

    @Override
    public boolean existsById(String id) {
        return execute(em -> em.find(Record.class, id) != null);
    }

    private <T> T execute(Function<EntityManager, T> action) {
        EntityManager em = emf.createEntityManager();
        try {
            return action.apply(em);
        } finally {
            em.close();
        }
    }

    private <T> T executeInTransaction(Function<EntityManager, T> action) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        try {
            tx.begin();
            T result = action.apply(em);
            tx.commit();
            return result;
        } catch (Exception e) {
            if (tx.isActive()) {
                tx.rollback();
            }
            throw e;
        } finally {
            em.close();
        }
    }

    private void executeInTransactionVoid(Consumer<EntityManager> action) {
        executeInTransaction(em -> {
            action.accept(em);
            return null;
        });
    }
}
