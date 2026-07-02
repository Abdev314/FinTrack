<script setup lang="ts">
import { ref, computed } from 'vue';
import { recordApi } from '../services/recordApi';
import { TransactionType, type RecordItem } from '../types/Records';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import {
  Download,
  X,
  FileSpreadsheet,
  FileText,
  FileType,
  FileJson,
  TrendingUp,
  TrendingDown,
  Wallet,
} from '@lucide/vue';

const isOpen = ref(false);
const loading = ref(false);
const downloading = ref<Record<'csv' | 'xlsx' | 'pdf' | 'json', boolean>>({
  csv: false,
  xlsx: false,
  pdf: false,
  json: false,
});
const error = ref<string | null>(null);
const records = ref<RecordItem[]>([]);

const totalIncome = computed(() =>
  records.value
    .filter((r) => r.transactionType === TransactionType.INCOME)
    .reduce((sum, r) => sum + r.amount, 0)
);

const totalExpense = computed(() =>
  records.value
    .filter((r) => r.transactionType === TransactionType.EXPENSE)
    .reduce((sum, r) => sum + r.amount, 0)
);

const balance = computed(() => totalIncome.value - totalExpense.value);

async function open() {
  isOpen.value = true;
  error.value = null;
  await loadRecords();
}

function close() {
  isOpen.value = false;
}

async function loadRecords() {
  loading.value = true;
  error.value = null;
  try {
    records.value = await recordApi.getAll();
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load records';
  } finally {
    loading.value = false;
  }
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

function triggerDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function recordsToCsv(data: RecordItem[]): string {
  const headers = ['Record ID', 'Type', 'Amount', 'Category', 'Date', 'Operator', 'Notes'];
  const rows = data.map((r) => [
    r.recordId,
    r.transactionType,
    r.amount,
    r.transactionCategory,
    r.date,
    r.operator,
    `"${(r.notes || '').replace(/"/g, '""')}"`,
  ]);
  return [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
}

async function downloadCsv() {
  downloading.value.csv = true;
  try {
    const csv = recordsToCsv(records.value);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    triggerDownload(blob, 'fintrack-records.csv');
  } finally {
    downloading.value.csv = false;
  }
}

async function downloadExcel() {
  downloading.value.xlsx = true;
  try {
    const rows = records.value.map((r) => ({
      'Record ID': r.recordId,
      Type: r.transactionType,
      Amount: r.amount,
      Category: r.transactionCategory,
      Date: r.date,
      Operator: r.operator,
      Notes: r.notes,
    }));
    const worksheet = XLSX.utils.json_to_sheet(rows);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Records');
    XLSX.writeFile(workbook, 'fintrack-records.xlsx');
  } finally {
    downloading.value.xlsx = false;
  }
}

async function downloadPdf() {
  downloading.value.pdf = true;
  try {
    const doc = new jsPDF({ orientation: 'landscape' });
    doc.setFontSize(16);
    doc.text('FinTrack Records', 14, 20);

    autoTable(doc, {
      startY: 28,
      head: [['Record ID', 'Type', 'Amount', 'Category', 'Date', 'Operator', 'Notes']],
      body: records.value.map((r) => [
        r.recordId,
        r.transactionType,
        r.amount.toString(),
        r.transactionCategory,
        r.date,
        r.operator,
        r.notes || '',
      ]),
      styles: { fontSize: 10, cellPadding: 2 },
      headStyles: { fillColor: [99, 102, 241] },
    });

    doc.save('fintrack-records.pdf');
  } finally {
    downloading.value.pdf = false;
  }
}

async function downloadJson() {
  downloading.value.json = true;
  try {
    const blob = new Blob([JSON.stringify(records.value, null, 2)], { type: 'application/json' });
    triggerDownload(blob, 'fintrack-records.json');
  } finally {
    downloading.value.json = false;
  }
}

const options = [
  {
    key: 'csv' as const,
    label: 'CSV',
    description: 'Plain text spreadsheet',
    icon: FileText,
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
    ring: 'ring-emerald-200',
    action: downloadCsv,
  },
  {
    key: 'xlsx' as const,
    label: 'Excel',
    description: 'Microsoft Excel workbook',
    icon: FileSpreadsheet,
    color: 'text-indigo-600',
    bg: 'bg-indigo-50',
    ring: 'ring-indigo-200',
    action: downloadExcel,
  },
  {
    key: 'pdf' as const,
    label: 'PDF',
    description: 'Printable document',
    icon: FileType,
    color: 'text-rose-600',
    bg: 'bg-rose-50',
    ring: 'ring-rose-200',
    action: downloadPdf,
  },
  {
    key: 'json' as const,
    label: 'JSON',
    description: 'Raw data export',
    icon: FileJson,
    color: 'text-amber-600',
    bg: 'bg-amber-50',
    ring: 'ring-amber-200',
    action: downloadJson,
  },
];
</script>

<template>
  <div>
    <button
      @click="open"
      class="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-700 shadow-sm ring-1 ring-slate-200 transition-all hover:bg-slate-50 hover:text-indigo-600 hover:ring-indigo-200 active:translate-y-0"
    >
      <Download class="h-4 w-4" />
      Export Records
    </button>

    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isOpen"
          class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/50 py-8 px-4"
          @click.self="close"
        >
          <Transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="opacity-0 scale-95 translate-y-2"
            enter-to-class="opacity-100 scale-100 translate-y-0"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="opacity-100 scale-100 translate-y-0"
            leave-to-class="opacity-0 scale-95 translate-y-2"
          >
            <div
              v-if="isOpen"
              class="w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-2xl bg-white shadow-2xl ring-1 ring-slate-900/5"
            >
            <div class="flex items-center justify-between border-b border-slate-100 px-6 py-4">
              <div>
                <h2 class="text-lg font-semibold text-slate-900">Export Records</h2>
                <p class="text-sm text-slate-500">Download your records in your preferred format</p>
              </div>
              <button
                @click="close"
                class="rounded-lg p-2 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600"
                aria-label="Close"
              >
                <X class="h-5 w-5" />
              </button>
            </div>

            <div class="p-6">
              <div v-if="loading" class="py-10 text-center text-slate-500">
                <span class="inline-block h-6 w-6 animate-spin rounded-full border-2 border-indigo-200 border-t-indigo-600"></span>
                <p class="mt-3 text-sm">Loading records...</p>
              </div>

              <template v-else>
                <div v-if="error" class="mb-5 rounded-xl bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
                  {{ error }}
                </div>

                <div class="mb-6 grid gap-4 sm:grid-cols-3">
                  <div class="rounded-2xl bg-emerald-50 p-4 ring-1 ring-emerald-100">
                    <div class="mb-2 flex items-center gap-2 text-emerald-700">
                      <TrendingUp class="h-5 w-5" />
                      <span class="text-sm font-medium">Total Income</span>
                    </div>
                    <p class="text-2xl font-bold text-emerald-800">{{ formatCurrency(totalIncome) }}</p>
                  </div>

                  <div class="rounded-2xl bg-rose-50 p-4 ring-1 ring-rose-100">
                    <div class="mb-2 flex items-center gap-2 text-rose-700">
                      <TrendingDown class="h-5 w-5" />
                      <span class="text-sm font-medium">Total Expense</span>
                    </div>
                    <p class="text-2xl font-bold text-rose-800">{{ formatCurrency(totalExpense) }}</p>
                  </div>

                  <div class="rounded-2xl bg-indigo-50 p-4 ring-1 ring-indigo-100">
                    <div class="mb-2 flex items-center gap-2 text-indigo-700">
                      <Wallet class="h-5 w-5" />
                      <span class="text-sm font-medium">Balance</span>
                    </div>
                    <p class="text-2xl font-bold text-indigo-800">{{ formatCurrency(balance) }}</p>
                  </div>
                </div>

                <p class="mb-4 text-sm font-medium text-slate-700">
                  {{ records.length }} record{{ records.length === 1 ? '' : 's' }} ready for export
                </p>

                <div class="grid gap-4 sm:grid-cols-2">
                  <button
                    v-for="option in options"
                    :key="option.key"
                    @click="option.action"
                    :disabled="downloading[option.key]"
                    class="group flex items-center gap-4 rounded-xl border border-slate-100 bg-slate-50 p-4 text-left transition-all hover:-translate-y-0.5 hover:bg-white hover:shadow-md hover:ring-1 hover:ring-slate-200 disabled:opacity-60"
                  >
                    <div
                      :class="`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl ${option.bg} ring-1 ${option.ring}`"
                    >
                      <component
                        :is="option.icon"
                        :class="`h-6 w-6 ${option.color}`"
                      />
                    </div>
                    <div class="flex-1">
                      <div class="flex items-center justify-between">
                        <span class="font-semibold text-slate-900">{{ option.label }}</span>
                        <span
                          v-if="downloading[option.key]"
                          class="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-indigo-600"
                        />
                      </div>
                      <p class="text-sm text-slate-500">{{ option.description }}</p>
                    </div>
                  </button>
                </div>
              </template>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
    </Teleport>
  </div>
</template>
