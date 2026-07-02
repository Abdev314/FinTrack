export enum TransactionType {
    INCOME = 'INCOME',
    EXPENSE = 'EXPENSE',
    TRANSFER = 'TRANSFER',
}

export enum TransactionCategory {
    SALARY = 'SALARY',
    RENT = 'RENT',
    TRANSPORT = 'TRANSPORT',
    SHOPPING = 'SHOPPING',
    FOOD = 'FOOD',
    ENTERTAINMENT = 'ENTERTAINMENT',
    OTHER = 'OTHER',
}

export interface RecordItem {
    recordId: string;
    transactionType: TransactionType;
    amount: number;
    transactionCategory: TransactionCategory;
    date: string;
    operator: string;
    notes: string;
}

export function getTransactionTypeLabel(type: TransactionType): string {
    switch (type) {
        case TransactionType.INCOME:
            return 'Income';
        case TransactionType.EXPENSE:
            return 'Expense';
        case TransactionType.TRANSFER:
            return 'Transfer';
        default:
            return type;
    }
}

export function getTransactionCategoryLabel(category: TransactionCategory): string {
    switch (category) {
        case TransactionCategory.SALARY:
            return 'Salary';
        case TransactionCategory.RENT:
            return 'Rent';
        case TransactionCategory.TRANSPORT:
            return 'Transport';
        case TransactionCategory.SHOPPING:
            return 'Shopping';
        case TransactionCategory.FOOD:
            return 'Food';
        case TransactionCategory.ENTERTAINMENT:
            return 'Entertainment';
        case TransactionCategory.OTHER:
            return 'Other';
        default:
            return category;
    }
}

export const TRANSACTION_TYPES: TransactionType[] = Object.values(TransactionType);
export const TRANSACTION_CATEGORIES: TransactionCategory[] = Object.values(TransactionCategory);
