package com.cms.web.fintrack.domain.model;

import com.cms.web.fintrack.domain.enums.TransactionType;
import com.cms.web.fintrack.domain.enums.TransactionCategory;

public class Record {

    private String RecordId;
    private TransactionType transactionType;
    private int Amount;
    private TransactionCategory transactionCategory;
    private String Date;
    private String Operator;
    private String Notes;

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
        Amount = amount;
        this.transactionCategory = transactionCategory;
        Date = date;
        Operator = operator;
        Notes = notes;
        RecordId = recordId;
    }

    //Getter

    public String getRecordId() {
        return RecordId;
    }

    public TransactionType getTransactionType() {
        return transactionType;
    }

    public int getAmount() {
        return Amount;
    }

    public TransactionCategory getTransactionCategory() {
        return transactionCategory;
    }

    public String getDate() {
        return Date;
    }

    public String getOperator() {
        return Operator;
    }

    public String getNotes() {
        return Notes;
    }

    //Setter
    public void setTransactionType(TransactionType transactionType) {
        this.transactionType = transactionType;
    }

    public void setAmount(int amount) {
        Amount = amount;
    }

    public void setTransactionCategory(TransactionCategory transactionCategory) {
        this.transactionCategory = transactionCategory;
    }

    public void setOperator(String operator) {
        Operator = operator;
    }

    public void setNotes(String notes) {
        Notes = notes;
    }
}
