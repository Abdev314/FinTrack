export enum TransactionType {
    INCOME = 'Income',
    EXPENSE = 'Expense',
    TRANSFER = 'Transfer',
}

export enum TransactionCategory {
    SALARY ='Salary',
    RENT ='Rent',
    TRANSPORT = 'Transport',
    SHOPPING = 'Shopping',
    FOOD = 'Food',
    ENTERTAINMENT = 'Entertainment',
    OTHER = 'Other',
}

export interface Record {
    recordId: string;
    transactionType: TransactionType;
    amount: number;
    transactionCategory: TransactionCategory;
    date: string;
    operator: string;
    notes: string;

}