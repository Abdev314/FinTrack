<script setup lang="ts">
import { computed, ref } from 'vue';
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

const downloading = ref<
  Record<'csv' | 'xlsx' | 'pdf' | 'json', boolean>
>({
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
  if (!Object.values(downloading.value).some(Boolean)) {
    isOpen.value = false;
  }
}

async function loadRecords() {
  loading.value = true;
  error.value = null;

  try {
    records.value = await recordApi.getAll();
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Failed to load records';
  } finally {
    loading.value = false;
  }
}

function formatCurrency(amount: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

function triggerDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');

  link.href = url;
  link.download = filename;

  document.body.appendChild(link);
  link.click();
  link.remove();

  URL.revokeObjectURL(url);
}

function recordsToCsv(data: RecordItem[]) {
  const headers = [
    'Record ID',
    'Type',
    'Amount',
    'Category',
    'Date',
    'Operator',
    'Notes',
  ];

  const rows = data.map((record) => [
    `"${record.recordId.replace(/"/g, '""')}"`,
    `"${record.transactionType.replace(/"/g, '""')}"`,
    record.amount,
    `"${record.transactionCategory.replace(/"/g, '""')}"`,
    `"${record.date}"`,
    `"${record.operator.replace(/"/g, '""')}"`,
    `"${(record.notes || '').replace(/"/g, '""')}"`,
  ]);

  return [
    headers.join(','),
    ...rows.map((row) => row.join(',')),
  ].join('\n');
}

async function downloadCsv() {
  downloading.value.csv = true;

  try {
    const csv = recordsToCsv(records.value);

    triggerDownload(
      new Blob([csv], { type: 'text/csv;charset=utf-8;' }),
      'fintrack-records.csv'
    );
  } finally {
    downloading.value.csv = false;
  }
}

async function downloadExcel() {
  downloading.value.xlsx = true;

  try {
    const rows = records.value.map((record) => ({
      'Record ID': record.recordId,
      Type: record.transactionType,
      Amount: record.amount,
      Category: record.transactionCategory,
      Date: record.date,
      Operator: record.operator,
      Notes: record.notes || '',
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
    const doc = new jsPDF({
      orientation: 'landscape',
    });

    doc.setFontSize(18);
    doc.text('FinTrack Records', 14, 18);

    doc.setFontSize(10);
    doc.text(
      `Income: ${formatCurrency(totalIncome.value)}`,
      14,
      25
    );

    doc.text(
      `Expense: ${formatCurrency(totalExpense.value)}`,
      75,
      25
    );

    doc.text(
      `Balance: ${formatCurrency(balance.value)}`,
      145,
      25
    );

    autoTable(doc, {
      startY: 32,

      head: [[
        'Record ID',
        'Type',
        'Amount',
        'Category',
        'Date',
        'Operator',
        'Notes',
      ]],

      body: records.value.map((record) => [
        record.recordId,
        record.transactionType,
        formatCurrency(record.amount),
        record.transactionCategory,
        record.date,
        record.operator,
        record.notes || '',
      ]),

      styles: {
        fontSize: 9,
        cellPadding: 3,
      },

      headStyles: {
        fillColor: [79, 70, 229],
      },
    });

    doc.save('fintrack-records.pdf');
  } finally {
    downloading.value.pdf = false;
  }
}

async function downloadJson() {
  downloading.value.json = true;

  try {
    const blob = new Blob(
      [JSON.stringify(records.value, null, 2)],
      { type: 'application/json' }
    );

    triggerDownload(blob, 'fintrack-records.json');
  } finally {
    downloading.value.json = false;
  }
}

const options = [
  {
    key: 'csv' as const,
    label: 'CSV',
    description: 'Simple spreadsheet format',
    icon: FileText,
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
  },
  {
    key: 'xlsx' as const,
    label: 'Excel',
    description: 'Microsoft Excel workbook',
    icon: FileSpreadsheet,
    color: 'text-indigo-600',
    bg: 'bg-indigo-50',
  },
  {
    key: 'pdf' as const,
    label: 'PDF',
    description: 'Printable document',
    icon: FileType,
    color: 'text-rose-600',
    bg: 'bg-rose-50',
  },
  {
    key: 'json' as const,
    label: 'JSON',
    description: 'Raw application data',
    icon: FileJson,
    color: 'text-amber-600',
    bg: 'bg-amber-50',
  },
];
</script>

<template>
  <div>
    <button
      type="button"
      @click="open"
      class="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm ring-1 ring-slate-100 transition-colors hover:bg-slate-50 hover:text-indigo-600"
    >
      <Download class="h-4 w-4" />
      <span>Export</span>
    </button>

    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-150 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-100 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isOpen"
          class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-slate-900/30 px-4 py-8"
          @click.self="close"
        >
          <div
            class="w-full max-w-2xl overflow-hidden rounded-2xl bg-white shadow-xl"
          >
            <!-- Header -->
            <div class="flex items-center justify-between border-b border-slate-100 px-5 py-4 sm:px-6">
              <div>
                <h2 class="text-lg font-semibold text-slate-900">
                  Export Records
                </h2>

                <p class="mt-0.5 text-sm text-slate-500">
                  Download your financial records
                </p>
              </div>

              <button
                type="button"
                @click="close"
                class="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
              >
                <X class="h-5 w-5" />
              </button>
            </div>

            <div class="max-h-[calc(100vh-8rem)] overflow-y-auto p-5 sm:p-6">
              <!-- Loading -->
              <div
                v-if="loading"
                class="flex flex-col items-center justify-center py-16"
              >
                <span
                  class="h-6 w-6 animate-spin rounded-full border-2 border-slate-200 border-t-indigo-600"
                />

                <p class="mt-3 text-sm text-slate-500">
                  Loading records...
                </p>
              </div>

              <template v-else>
                <!-- Error -->
                <div
                  v-if="error"
                  class="mb-5 rounded-xl bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700"
                >
                  {{ error }}
                </div>

                <!-- Summary -->
                <div class="grid gap-3 sm:grid-cols-3">
                  <div class="rounded-xl bg-emerald-50 p-4">
                    <div class="flex items-center gap-2 text-emerald-600">
                      <TrendingUp class="h-4 w-4" />
                      <span class="text-xs font-medium">Income</span>
                    </div>

                    <p class="mt-2 text-lg font-semibold text-emerald-700">
                      {{ formatCurrency(totalIncome) }}
                    </p>
                  </div>

                  <div class="rounded-xl bg-rose-50 p-4">
                    <div class="flex items-center gap-2 text-rose-600">
                      <TrendingDown class="h-4 w-4" />
                      <span class="text-xs font-medium">Expense</span>
                    </div>

                    <p class="mt-2 text-lg font-semibold text-rose-700">
                      {{ formatCurrency(totalExpense) }}
                    </p>
                  </div>

                  <div class="rounded-xl bg-indigo-50 p-4">
                    <div class="flex items-center gap-2 text-indigo-600">
                      <Wallet class="h-4 w-4" />
                      <span class="text-xs font-medium">Balance</span>
                    </div>

                    <p class="mt-2 text-lg font-semibold text-indigo-700">
                      {{ formatCurrency(balance) }}
                    </p>
                  </div>
                </div>

                <!-- Export options -->
                <div class="mt-6">
                  <div class="mb-3 flex items-center justify-between">
                    <p class="text-sm font-semibold text-slate-900">
                      Export format
                    </p>

                    <span class="text-xs text-slate-400">
                      {{ records.length }}
                      {{ records.length === 1 ? 'record' : 'records' }}
                    </span>
                  </div>

                  <div class="grid gap-3 sm:grid-cols-2">
                    <button
                      v-for="option in options"
                      :key="option.key"
                      type="button"
                      @click="option.key === 'csv'
                        ? downloadCsv()
                        : option.key === 'xlsx'
                        ? downloadExcel()
                        : option.key === 'pdf'
                        ? downloadPdf()
                        : downloadJson()"
                      :disabled="
                        downloading[option.key] ||
                        records.length === 0
                      "
                      class="flex items-center gap-3 rounded-xl bg-white p-4 text-left shadow-sm ring-1 ring-slate-100 transition-all hover:-translate-y-0.5 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      <div
                        :class="[
                          'flex h-10 w-10 shrink-0 items-center justify-center rounded-xl',
                          option.bg,
                        ]"
                      >
                        <component
                          :is="option.icon"
                          class="h-5 w-5"
                          :class="option.color"
                        />
                      </div>

                      <div class="min-w-0 flex-1">
                        <div class="flex items-center justify-between gap-3">
                          <span class="text-sm font-semibold text-slate-900">
                            {{ option.label }}
                          </span>

                          <span
                            v-if="downloading[option.key]"
                            class="h-4 w-4 shrink-0 animate-spin rounded-full border-2 border-slate-200 border-t-indigo-600"
                          />
                        </div>

                        <p class="mt-0.5 text-xs text-slate-500">
                          {{ option.description }}
                        </p>
                      </div>
                    </button>
                  </div>

                  <p
                    v-if="records.length === 0"
                    class="mt-4 text-center text-sm text-slate-400"
                  >
                    There are no records to export.
                  </p>
                </div>
              </template>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>