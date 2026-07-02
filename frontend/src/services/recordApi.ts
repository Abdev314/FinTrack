import {type Record, TransactionCategory, TransactionType} from "../types/Records";
const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const recordApi = {
    create: (record: Record): Promise<Record> =>
        fetch(`${API_BASE}/records`, {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(record),
        }).then((res) => {
            if(!res.ok) throw new Error('Failed to create a record')
            return res.json();
        }),

    getById: (id: string): Promise<Record> =>
        fetch(`${API_BASE}/records/${id}`).then((res => {
            if(!res.ok) throw new Error('Record not found')
            return res.json();
        })),

    getByType: (type: TransactionType): Promise<Record[]> =>
        fetch(`${API_BASE}/records/type/${type}`).then((res) => {
            if (!res.ok) throw new Error("Failed to fetch records");
            return res.json();
        }),

    getByCategory: (category: TransactionCategory): Promise<Record[]> =>
        fetch(`${API_BASE}/records/category/${category}`).then((res) => {
            if (!res.ok) throw new Error("Failed to fetch records");
            return res.json();
        }),

    getAll: (): Promise<Record[]> =>
        fetch(`${API_BASE}/records`).then((res) => {
            if (!res.ok) throw new Error("Failed to fetch records");
            return res.json();
        }),

    delete: (id: string): Promise<void> =>
        fetch(`${API_BASE}/records/${id}`, {
            method: "DELETE",
        }).then((res) => {
            if (!res.ok) throw new Error("Failed to delete record");
            // No content returned (204)
        }),
} as const;
