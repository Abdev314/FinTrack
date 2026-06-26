package com.web.fintrack.domain.model;

import com.web.fintrack.domain.enums.TransactionType;
import com.web.fintrack.domain.enums.TransactionCategory;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "records")
public class Record {

    @Id
    @Column(name = "record_id")
    private String recordId;

    @Enumerated(EnumType.STRING)
    @Column(name = "transaction_type")
    private TransactionType transactionType;

    @Column(name = "amount")
    private int amount;

    @Enumerated(EnumType.STRING)
    @Column(name = "transaction_category")
    private TransactionCategory transactionCategory;

    @Column(name = "record_date")
    private String date;

    @Column(name = "operator")
    private String operator;

    @Column(name = "notes")
    private String notes;

    public Record() {
    }

    public Record(
            TransactionType transactionType,
            int amount,
            TransactionCategory transactionCategory,
            String date,
            String operator,
            String notes,
            String recordId
    ) {
        this.transactionType = transactionType;
        this.amount = amount;
        this.transactionCategory = transactionCategory;
        this.date = date;
        this.operator = operator;
        this.notes = notes;
        this.recordId = recordId;
    }

    public String getRecordId() {
        return recordId;
    }

    public void setRecordId(String recordId) {
        this.recordId = recordId;
    }

    public TransactionType getTransactionType() {
        return transactionType;
    }

    public void setTransactionType(TransactionType transactionType) {
        this.transactionType = transactionType;
    }

    public int getAmount() {
        return amount;
    }

    public void setAmount(int amount) {
        this.amount = amount;
    }

    public TransactionCategory getTransactionCategory() {
        return transactionCategory;
    }

    public void setTransactionCategory(TransactionCategory transactionCategory) {
        this.transactionCategory = transactionCategory;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getOperator() {
        return operator;
    }

    public void setOperator(String operator) {
        this.operator = operator;
    }

    public String getNotes() {
        return notes;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }
}
