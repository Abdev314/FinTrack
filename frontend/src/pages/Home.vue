<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import AddRecordForm from '../components/AddRecordForm.vue';
import EditRecordForm from '../components/EditRecordForm.vue';
import DownloadRecord from '../components/DownloadRecord.vue';
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
  <div class="min-h-screen bg-slate-50 py-8 sm:py-12 lg:py-16">
    <header class="sticky top-0 z-30 border-b border-slate-100 bg-white/80 backdrop-blur-md">
      <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-md shadow-indigo-200">
            <Wallet class="h-6 w-6" />
          </div>
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-900">FinTrack</h1>
            <p class="text-xs text-slate-500">Income & Expense Management</p>
          </div>
        </div>

        <div class="flex items-center gap-2 sm:gap-3">
          <DownloadRecord />
          <EditRecordForm @updated="loadRecords" />
          <AddRecordForm @added="loadRecords" />
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div class="mb-6 grid gap-4 sm:grid-cols-3">
        <div class="rounded-2xl bg-emerald-50 p-5 ring-1 ring-emerald-100">
          <div class="mb-2 flex items-center gap-2 text-emerald-700">
            <TrendingUp class="h-5 w-5" />
            <span class="text-sm font-medium">Total Income</span>
          </div>
          <p class="text-2xl font-bold text-emerald-800">{{ formatCurrency(totalIncome) }}</p>
        </div>

        <div class="rounded-2xl bg-rose-50 p-5 ring-1 ring-rose-100">
          <div class="mb-2 flex items-center gap-2 text-rose-700">
            <TrendingDown class="h-5 w-5" />
            <span class="text-sm font-medium">Total Expense</span>
          </div>
          <p class="text-2xl font-bold text-rose-800">{{ formatCurrency(totalExpense) }}</p>
        </div>

        <div class="rounded-2xl bg-indigo-50 p-5 ring-1 ring-indigo-100">
          <div class="mb-2 flex items-center gap-2 text-indigo-700">
            <Wallet class="h-5 w-5" />
            <span class="text-sm font-medium">Balance</span>
          </div>
          <p class="text-2xl font-bold text-indigo-800">{{ formatCurrency(balance) }}</p>
        </div>
      </div>

      <div v-if="error" class="mb-5 rounded-xl bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
        {{ error }}
      </div>

      <div class="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-slate-200">
        <div class="border-b border-slate-100 px-6 py-4">
          <h2 class="text-lg font-semibold text-slate-900">Records</h2>
          <p class="text-sm text-slate-500">Manage your income and expense transactions</p>
        </div>

        <div v-if="loading" class="py-16 text-center text-slate-500">
          <span class="inline-block h-8 w-8 animate-spin rounded-full border-2 border-indigo-200 border-t-indigo-600"></span>
          <p class="mt-3 text-sm">Loading records...</p>
        </div>

        <div v-else-if="records.length === 0" class="py-16 text-center">
          <div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-100 text-slate-400">
            <FileText class="h-7 w-7" />
          </div>
          <p class="text-slate-900 font-medium">No records yet</p>
          <p class="mt-1 text-sm text-slate-500">Click "Add Record" to create your first transaction.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead class="bg-slate-50 text-slate-600">
              <tr>
                <th class="px-6 py-3.5 font-semibold">ID</th>
                <th class="px-6 py-3.5 font-semibold">Type</th>
                <th class="px-6 py-3.5 font-semibold">Amount</th>
                <th class="px-6 py-3.5 font-semibold">Category</th>
                <th class="px-6 py-3.5 font-semibold">Date</th>
                <th class="px-6 py-3.5 font-semibold">Operator</th>
                <th class="px-6 py-3.5 font-semibold">Notes</th>
                <th class="px-6 py-3.5 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr
                v-for="record in records"
                :key="record.recordId"
                class="transition-colors hover:bg-slate-50"
              >
                <td class="px-6 py-4 font-medium text-slate-900">{{ record.recordId }}</td>
                <td class="px-6 py-4">
                  <span
                    :class="[
                      'inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium',
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
                      class="h-3.5 w-3.5"
                    />
                    {{ record.transactionType }}
                  </span>
                </td>
                <td class="px-6 py-4 font-medium text-slate-900">{{ formatCurrency(record.amount) }}</td>
                <td class="px-6 py-4 text-slate-600">{{ record.transactionCategory }}</td>
                <td class="px-6 py-4 text-slate-600">{{ record.date }}</td>
                <td class="px-6 py-4 text-slate-600">{{ record.operator }}</td>
                <td class="px-6 py-4 text-slate-600">{{ record.notes || '-' }}</td>
                <td class="px-6 py-4 text-right">
                  <button
                    @click="openDeleteModal(record.recordId)"
                    class="inline-flex items-center gap-1.5 rounded-lg p-2 text-rose-500 transition-colors hover:bg-rose-50"
                    aria-label="Delete record"
                  >
                    <Trash2 class="h-4 w-4" />
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
          class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/50 py-8 px-4"
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
              class="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl ring-1 ring-slate-900/5"
            >
              <div class="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-rose-50 text-rose-600">
                <AlertTriangle class="h-7 w-7" />
              </div>

              <h3 class="text-lg font-semibold text-slate-900">Delete Record?</h3>
              <p class="mt-2 text-sm text-slate-500">
                Are you sure you want to delete this record? This action cannot be undone.
              </p>

              <div class="mt-6 flex items-center justify-end gap-3">
                <button
                  @click="closeDeleteModal"
                  class="rounded-xl px-5 py-2.5 text-sm font-semibold text-slate-600 transition-colors hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  @click="confirmDelete"
                  :disabled="deleting"
                  class="inline-flex items-center gap-2 rounded-xl bg-rose-600 px-5 py-2.5 text-sm font-semibold text-white shadow-md shadow-rose-200 transition-all hover:bg-rose-700 disabled:opacity-60"
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
