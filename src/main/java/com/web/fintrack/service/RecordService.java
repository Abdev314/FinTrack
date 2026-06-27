package com.web.fintrack.service;

import com.web.fintrack.dao.RecordRepositoryImpl;
import com.web.fintrack.domain.model.Record;
import com.web.fintrack.repository.RecordRepository;

import java.util.List;
import java.util.Optional;


public class RecordService {

    private final RecordRepository<Record, String> recordRepository;

    public RecordService() {
        this.recordRepository = new RecordRepositoryImpl();
    }

    public RecordService(RecordRepository<Record, String> recordRepository) {
        this.recordRepository = recordRepository;
    }

    public Record create(Record record) {
        if (record == null) {
            throw new IllegalArgumentException("Record cannot be null");
        }
        if (record.getRecordId() == null || record.getRecordId().trim().isEmpty()) {
            throw new IllegalArgumentException("Record ID is required");
        }

        if (record.getAmount() <= 0) {
            throw new IllegalArgumentException("Amount must be greater than zero");
        }

        if (record.getTransactionType() == null) {
            throw new IllegalArgumentException("Transaction Type is required");
        }

        if (recordRepository.existsById(record.getRecordId())) {
            throw new IllegalArgumentException("Record with ID '" + record.getRecordId() + "' already exists");
        }
        return recordRepository.save(record);
    }

    public Optional<Record> findById(Record record) {
        return recordRepository.findById(record.getRecordId());
    }

    public List<Record> findByType(Record record){
        return recordRepository.findByType(record.getTransactionType());
    }

    public List<Record> findByCategory(Record record){
        return  recordRepository.findByCategory(record.getTransactionCategory());
    }

    public List<Record> findAll(){
        return recordRepository.findAll();
    }

    public void deleteRecord(Record record) {
        if (record == null || record.getRecordId() == null || record.getRecordId().trim().isEmpty()) {
            throw new IllegalArgumentException("Record ID is required");
        }
        if (!recordRepository.existsById(record.getRecordId())) {
            throw new IllegalArgumentException("Record with ID '" + record.getRecordId() + "' not found");
        }
        recordRepository.deleteById(record.getRecordId());
    }
}
