# FinTrack Test Commands

This file contains HTTP test commands for the application and useful SQL queries for the PostgreSQL database.

---

## Application Base URL

```text
http://localhost:8080/FinTrack/api
```

---

## cURL Test Commands

### 1. Create a new record (POST /api/records)

```bash
curl -X POST http://localhost:8080/FinTrack/api/records \
  -H "Content-Type: application/json" \
  -d '{
    "recordId": "rec-001",
    "transactionType": "INCOME",
    "amount": 5000,
    "transactionCategory": "SALARY",
    "date": "2026-06-27",
    "operator": "admin",
    "notes": "Monthly salary"
  }'
```

### 2. Create another record (expense)

```bash
curl -X POST http://localhost:8080/FinTrack/api/records \
  -H "Content-Type: application/json" \
  -d '{
    "recordId": "rec-002",
    "transactionType": "EXPENSE",
    "amount": 150,
    "transactionCategory": "FOOD",
    "date": "2026-06-27",
    "operator": "admin",
    "notes": "Lunch"
  }'
```

### 3. Get all records (GET /api/records)

```bash
curl -X GET http://localhost:8080/FinTrack/api/records
```

### 4. Get record by ID (GET /api/records/{id})

```bash
curl -X GET http://localhost:8080/FinTrack/api/records/rec-001
```

### 5. Get records by type (GET /api/records/type/{type})

```bash
curl -X GET http://localhost:8080/FinTrack/api/records/type/INCOME
```

### 6. Get records by category (GET /api/records/category/{category})

```bash
curl -X GET http://localhost:8080/FinTrack/api/records/category/SALARY
```

### 7. Delete a record (DELETE /api/records/{id})

```bash
curl -X DELETE http://localhost:8080/FinTrack/api/records/rec-002
```

### 8. Try to get a deleted record (should return 404)

```bash
curl -X GET http://localhost:8080/FinTrack/api/records/rec-002
```

---

## PostgreSQL Terminal Queries

### Connect to the database

```bash
psql -h localhost -p 5432 -U fintrack_user -d fintrack
```

When prompted, enter the password:

```text
fintrack_password
```

### List all tables

```sql
\dt
```

### Describe the records table

```sql
\d records
```

### Select all records

```sql
SELECT * FROM records;
```

### Select records by type

```sql
SELECT * FROM records WHERE transaction_type = 'INCOME';
```

### Select records by category

```sql
SELECT * FROM records WHERE transaction_category = 'SALARY';
```

### Count total records

```sql
SELECT COUNT(*) FROM records;
```

### Insert a record directly

```sql
INSERT INTO records (record_id, transaction_type, amount, transaction_category, record_date, operator, notes)
VALUES ('rec-003', 'EXPENSE', 75, 'TRANSPORT', '2026-06-28', 'admin', 'Bus ticket');
```

### Delete a record by ID

```sql
DELETE FROM records WHERE record_id = 'rec-003';
```

### Delete all records

```sql
DELETE FROM records;
```

### Drop the records table (use with caution)

```sql
DROP TABLE records;
```

### Exit psql

```sql
\q
```
