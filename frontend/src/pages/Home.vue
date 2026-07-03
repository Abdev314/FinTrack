<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import AddRecordForm from '../components/AddRecordForm.vue';
import EditRecordForm from '../components/EditRecordForm.vue';
import DownloadRecord from '../components/DownloadRecord.vue';
import SearchRecord from '../components/SearchRecord.vue';
import { recordApi } from '../services/recordApi';
import { TransactionType, type RecordItem } from '../types/Records';
import {
  Wallet,
  TrendingUp,
  TrendingDown,
  Trash2,
  FileText,
  AlertTriangle,
} from '@lucide/vue';

const records = ref<RecordItem[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const showDeleteModal = ref(false);
const recordToDelete = ref<string | null>(null);
const deleting = ref(false);

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

function openDeleteModal(id: string) {
  recordToDelete.value = id;
  showDeleteModal.value = true;
}

function closeDeleteModal() {
  showDeleteModal.value = false;
  recordToDelete.value = null;
}

async function confirmDelete() {
  if (!recordToDelete.value) return;
  deleting.value = true;
  error.value = null;
  try {
    await recordApi.delete(recordToDelete.value);
    await loadRecords();
    closeDeleteModal();
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to delete record';
  } finally {
    deleting.value = false;
  }
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

onMounted(loadRecords);
</script>

<template>
  <div class="min-h-screen bg-slate-50 py-0 sm:py-0 md:py-8 lg:py-12">
    <header class="sticky top-0 z-30 border-b border-slate-100 bg-white/90 backdrop-blur-md">
      <div class="mx-auto flex h-auto min-h-16 max-w-7xl flex-col items-stretch justify-between gap-3 px-4 py-3 sm:flex-row sm:items-center sm:px-6 lg:px-8">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-md shadow-indigo-200">
            <Wallet class="h-6 w-6" />
          </div>
          <div>
            <h1 class="text-lg font-bold tracking-tight text-slate-900 sm:text-xl">FinTrack</h1>
            <p class="text-xs text-slate-500">Income & Expense Management</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2 sm:flex sm:items-center sm:gap-2 lg:gap-3">
          <SearchRecord />
          <DownloadRecord />
          <EditRecordForm @updated="loadRecords" />
          <AddRecordForm @added="loadRecords" />
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-3 py-5 sm:px-4 md:px-6 md:py-8 lg:px-8">
      <div class="mb-6 rounded-2xl bg-gradient-to-r from-indigo-500 to-violet-500 p-5 text-white shadow-lg shadow-indigo-200 sm:mb-8 sm:p-8">
        <div class="max-w-2xl">
          <h2 class="text-xl font-bold tracking-tight sm:text-2xl lg:text-3xl">Welcome to FinTrack</h2>
          <p class="mt-1 text-sm text-indigo-100 sm:mt-2 sm:text-base">
            Track your income and expenses with ease. Stay on top of your finances, one record at a time.
          </p>
        </div>
      </div>

      <div class="mb-6 grid gap-3 sm:grid-cols-3 lg:gap-4">
        <div class="rounded-2xl bg-emerald-50 p-4 ring-1 ring-emerald-100 sm:p-5">
          <div class="mb-1 flex items-center gap-2 text-emerald-700 sm:mb-2">
            <TrendingUp class="h-4 w-4 sm:h-5 sm:w-5" />
            <span class="text-xs font-medium sm:text-sm">Total Income</span>
          </div>
          <p class="text-xl font-bold text-emerald-800 sm:text-2xl">{{ formatCurrency(totalIncome) }}</p>
        </div>

        <div class="rounded-2xl bg-rose-50 p-4 ring-1 ring-rose-100 sm:p-5">
          <div class="mb-1 flex items-center gap-2 text-rose-700 sm:mb-2">
            <TrendingDown class="h-4 w-4 sm:h-5 sm:w-5" />
            <span class="text-xs font-medium sm:text-sm">Total Expense</span>
          </div>
          <p class="text-xl font-bold text-rose-800 sm:text-2xl">{{ formatCurrency(totalExpense) }}</p>
        </div>

        <div class="rounded-2xl bg-indigo-50 p-4 ring-1 ring-indigo-100 sm:p-5">
          <div class="mb-1 flex items-center gap-2 text-indigo-700 sm:mb-2">
            <Wallet class="h-4 w-4 sm:h-5 sm:w-5" />
            <span class="text-xs font-medium sm:text-sm">Balance</span>
          </div>
          <p class="text-xl font-bold text-indigo-800 sm:text-2xl">{{ formatCurrency(balance) }}</p>
        </div>
      </div>

      <div v-if="error" class="mb-4 rounded-xl bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700 sm:mb-5">
        {{ error }}
      </div>

      <div class="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-slate-200">
        <div class="border-b border-slate-100 px-4 py-3 sm:px-6 sm:py-4">
          <h2 class="text-base font-semibold text-slate-900 sm:text-lg">Records</h2>
          <p class="text-xs text-slate-500 sm:text-sm">Manage your income and expense transactions</p>
        </div>

        <div v-if="loading" class="py-12 text-center text-slate-500 sm:py-16">
          <span class="inline-block h-6 w-6 animate-spin rounded-full border-2 border-indigo-200 border-t-indigo-600 sm:h-8 sm:w-8"></span>
          <p class="mt-3 text-sm">Loading records...</p>
        </div>

        <div v-else-if="records.length === 0" class="py-12 text-center sm:py-16">
          <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-400 sm:h-14 sm:w-14">
            <FileText class="h-6 w-6 sm:h-7 sm:w-7" />
          </div>
          <p class="font-medium text-slate-900">No records yet</p>
          <p class="mt-1 text-sm text-slate-500">Click "Add Record" to create your first transaction.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full min-w-[640px] text-left text-sm">
            <thead class="bg-slate-50 text-slate-600">
              <tr>
                <th class="px-4 py-3 text-xs font-semibold sm:px-6 sm:py-3.5 sm:text-sm">ID</th>
                <th class="px-4 py-3 text-xs font-semibold sm:px-6 sm:py-3.5 sm:text-sm">Type</th>
                <th class="px-4 py-3 text-xs font-semibold sm:px-6 sm:py-3.5 sm:text-sm">Amount</th>
                <th class="px-4 py-3 text-xs font-semibold sm:px-6 sm:py-3.5 sm:text-sm">Category</th>
                <th class="px-4 py-3 text-xs font-semibold sm:px-6 sm:py-3.5 sm:text-sm">Date</th>
                <th class="px-4 py-3 text-xs font-semibold sm:px-6 sm:py-3.5 sm:text-sm">Operator</th>
                <th class="px-4 py-3 text-xs font-semibold sm:px-6 sm:py-3.5 sm:text-sm">Notes</th>
                <th class="px-4 py-3 text-right text-xs font-semibold sm:px-6 sm:py-3.5 sm:text-sm">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr
                v-for="record in records"
                :key="record.recordId"
                class="transition-colors hover:bg-slate-50"
              >
                <td class="px-4 py-3 text-xs font-medium text-slate-900 sm:px-6 sm:py-4 sm:text-sm">{{ record.recordId }}</td>
                <td class="px-4 py-3 sm:px-6 sm:py-4">
                  <span
                    :class="[
                      'inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-medium sm:gap-1.5 sm:px-2.5 sm:py-1 sm:text-xs',
                      record.transactionType === TransactionType.INCOME
                        ? 'bg-emerald-100 text-emerald-700'
                        : record.transactionType === TransactionType.EXPENSE
                        ? 'bg-rose-100 text-rose-700'
                        : 'bg-indigo-100 text-indigo-700',
                    ]"
                  >
                    <component
                      :is="
                        record.transactionType === TransactionType.INCOME
                          ? TrendingUp
                          : record.transactionType === TransactionType.EXPENSE
                          ? TrendingDown
                          : Wallet
                      "
                      class="h-3 w-3 sm:h-3.5 sm:w-3.5"
                    />
                    {{ record.transactionType }}
                  </span>
                </td>
                <td class="px-4 py-3 text-xs font-medium text-slate-900 sm:px-6 sm:py-4 sm:text-sm">{{ formatCurrency(record.amount) }}</td>
                <td class="px-4 py-3 text-xs text-slate-600 sm:px-6 sm:py-4 sm:text-sm">{{ record.transactionCategory }}</td>
                <td class="px-4 py-3 text-xs text-slate-600 sm:px-6 sm:py-4 sm:text-sm">{{ record.date }}</td>
                <td class="px-4 py-3 text-xs text-slate-600 sm:px-6 sm:py-4 sm:text-sm">{{ record.operator }}</td>
                <td class="px-4 py-3 text-xs text-slate-600 sm:px-6 sm:py-4 sm:text-sm">{{ record.notes || '-' }}</td>
                <td class="px-4 py-3 text-right sm:px-6 sm:py-4">
                  <button
                    @click="openDeleteModal(record.recordId)"
                    class="inline-flex items-center gap-1 rounded-lg p-1.5 text-rose-500 transition-colors hover:bg-rose-50 sm:gap-1.5 sm:p-2"
                    aria-label="Delete record"
                  >
                    <Trash2 class="h-3.5 w-3.5 sm:h-4 sm:w-4" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

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
          v-if="showDeleteModal"
          class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/50 px-4 py-8"
          @click.self="closeDeleteModal"
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
              v-if="showDeleteModal"
              class="w-full max-w-md rounded-2xl bg-white p-5 shadow-2xl ring-1 ring-slate-900/5 sm:p-6"
            >
              <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-50 text-rose-600 sm:mb-5 sm:h-14 sm:w-14">
                <AlertTriangle class="h-6 w-6 sm:h-7 sm:w-7" />
              </div>

              <h3 class="text-base font-semibold text-slate-900 sm:text-lg">Delete Record?</h3>
              <p class="mt-2 text-sm text-slate-500">
                Are you sure you want to delete this record? This action cannot be undone.
              </p>

              <div class="mt-5 flex items-center justify-end gap-3 sm:mt-6">
                <button
                  @click="closeDeleteModal"
                  class="rounded-xl px-4 py-2 text-sm font-semibold text-slate-600 transition-colors hover:bg-slate-100 sm:px-5 sm:py-2.5"
                >
                  Cancel
                </button>
                <button
                  @click="confirmDelete"
                  :disabled="deleting"
                  class="inline-flex items-center gap-2 rounded-xl bg-rose-600 px-4 py-2 text-sm font-semibold text-white shadow-md shadow-rose-200 transition-all hover:bg-rose-700 disabled:opacity-60 sm:px-5 sm:py-2.5"
                >
                  <span v-if="deleting" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                  {{ deleting ? 'Deleting...' : 'Delete' }}
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
