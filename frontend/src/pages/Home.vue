```vue
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
  ArrowUpRight,
  ArrowDownRight,
  Plus,
  ChevronRight,
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
    error.value =
      err instanceof Error ? err.message : 'Failed to load records';
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
    error.value =
      err instanceof Error ? err.message : 'Failed to delete record';
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

function isIncome(record: RecordItem) {
  return record.transactionType === TransactionType.INCOME;
}

function isExpense(record: RecordItem) {
  return record.transactionType === TransactionType.EXPENSE;
}

function typeIcon(record: RecordItem) {
  if (isIncome(record)) return ArrowDownRight;
  if (isExpense(record)) return ArrowUpRight;
  return Wallet;
}

function typeIconClass(record: RecordItem) {
  if (isIncome(record)) {
    return 'bg-emerald-50 text-emerald-600';
  }

  if (isExpense(record)) {
    return 'bg-rose-50 text-rose-600';
  }

  return 'bg-indigo-50 text-indigo-600';
}

function amountClass(record: RecordItem) {
  if (isIncome(record)) return 'text-emerald-600';
  if (isExpense(record)) return 'text-slate-900';
  return 'text-indigo-600';
}

onMounted(loadRecords);
</script>

<template>
  <div class="min-h-screen bg-white text-slate-900">

    <!-- Header -->
    <header class="border-b border-slate-100 bg-white">
      <div
        class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8"
      >
        <div class="flex items-center gap-3">
          <div
            class="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-white"
          >
            <Wallet class="h-5 w-5" />
          </div>

          <div>
            <h1 class="text-base font-semibold tracking-tight">
              FinTrack
            </h1>

            <p class="hidden text-xs text-slate-400 sm:block">
              Personal finance
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <SearchRecord />
          <DownloadRecord />
          <EditRecordForm @updated="loadRecords" />
          <AddRecordForm @added="loadRecords" />
        </div>
      </div>
    </header>

    <!-- Main -->
    <main
      class="mx-auto max-w-6xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8"
    >

      <!-- Greeting -->
      <div class="mb-6">
        <p class="text-sm font-medium text-slate-400">
          Welcome back
        </p>

        <h2
          class="mt-1 text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl"
        >
          Your finances
        </h2>
      </div>

      <!-- Balance Card -->
      <section
        class="relative overflow-hidden rounded-2xl bg-indigo-600 p-5 text-white shadow-sm sm:p-7"
      >
        <div class="relative z-10">

          <div class="flex items-start justify-between">
            <div>
              <p class="text-sm font-medium text-indigo-100">
                Total Balance
              </p>

              <p
                class="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl"
              >
                {{ formatCurrency(balance) }}
              </p>
            </div>

            <div
              class="flex items-center gap-1 rounded-full bg-white/15 px-2.5 py-1 text-xs font-medium"
            >
              <TrendingUp class="h-3.5 w-3.5" />
              Healthy
            </div>
          </div>

          <div class="mt-7 flex flex-col gap-2 sm:flex-row">

            <button
              class="flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-indigo-700 transition hover:bg-indigo-50"
            >
              <ArrowUpRight class="h-4 w-4" />
              Transfer
            </button>

            <button
              class="flex items-center justify-center gap-2 rounded-xl bg-indigo-500 px-4 py-2.5 text-sm font-semibold text-white ring-1 ring-white/20 transition hover:bg-indigo-400"
            >
              <Plus class="h-4 w-4" />
              Add Funds
            </button>

          </div>
        </div>

        <!-- Very subtle decoration -->
        <div
          class="absolute -right-16 -top-16 h-48 w-48 rounded-full bg-white/5"
        ></div>

        <div
          class="absolute -bottom-24 right-12 h-52 w-52 rounded-full bg-white/5"
        ></div>
      </section>

      <!-- Summary Cards -->
      <section class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3">

        <!-- Income -->
        <div
          class="rounded-2xl bg-white p-4 shadow-sm sm:p-5"
        >
          <div class="flex items-center gap-2">
            <div
              class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50 text-emerald-600"
            >
              <TrendingUp class="h-4 w-4" />
            </div>

            <span class="text-xs font-medium text-slate-400">
              Income
            </span>
          </div>

          <p
            class="mt-3 text-lg font-semibold tracking-tight text-slate-900 sm:text-xl"
          >
            {{ formatCurrency(totalIncome) }}
          </p>
        </div>

        <!-- Expense -->
        <div
          class="rounded-2xl bg-white p-4 shadow-sm sm:p-5"
        >
          <div class="flex items-center gap-2">
            <div
              class="flex h-8 w-8 items-center justify-center rounded-lg bg-rose-50 text-rose-600"
            >
              <TrendingDown class="h-4 w-4" />
            </div>

            <span class="text-xs font-medium text-slate-400">
              Expenses
            </span>
          </div>

          <p
            class="mt-3 text-lg font-semibold tracking-tight text-slate-900 sm:text-xl"
          >
            {{ formatCurrency(totalExpense) }}
          </p>
        </div>

        <!-- Balance -->
        <div
          class="col-span-2 rounded-2xl bg-white p-4 shadow-sm sm:col-span-1 sm:p-5"
        >
          <div class="flex items-center gap-2">
            <div
              class="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600"
            >
              <Wallet class="h-4 w-4" />
            </div>

            <span class="text-xs font-medium text-slate-400">
              Available
            </span>
          </div>

          <p
            class="mt-3 text-lg font-semibold tracking-tight text-slate-900 sm:text-xl"
          >
            {{ formatCurrency(balance) }}
          </p>
        </div>

      </section>

      <!-- Error -->
      <div
        v-if="error"
        class="mt-4 rounded-xl bg-rose-50 px-4 py-3 text-sm text-rose-700"
      >
        {{ error }}
      </div>

      <!-- Transactions -->
      <section class="mt-8">

        <!-- Section Header -->
        <div class="mb-4 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-semibold tracking-tight">
              Recent Transactions
            </h2>

            <p class="mt-0.5 text-xs text-slate-400">
              Your latest financial activity
            </p>
          </div>

          <button
            class="flex items-center gap-1 text-xs font-medium text-indigo-600 transition hover:text-indigo-700"
          >
            View all
            <ChevronRight class="h-4 w-4" />
          </button>
        </div>

        <!-- Loading -->
        <div
          v-if="loading"
          class="rounded-2xl bg-white py-14 text-center shadow-sm"
        >
          <span
            class="inline-block h-7 w-7 animate-spin rounded-full border-2 border-slate-200 border-t-indigo-600"
          ></span>

          <p class="mt-3 text-sm text-slate-400">
            Loading transactions...
          </p>
        </div>

        <!-- Empty -->
        <div
          v-else-if="records.length === 0"
          class="rounded-2xl bg-white px-5 py-14 text-center shadow-sm"
        >
          <div
            class="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-slate-50 text-slate-400"
          >
            <FileText class="h-6 w-6" />
          </div>

          <p class="mt-4 text-sm font-medium text-slate-900">
            No transactions yet
          </p>

          <p class="mt-1 text-xs text-slate-400">
            Add your first record to start tracking your finances.
          </p>
        </div>

        <!-- Mobile Transactions -->
        <div
          v-else
          class="space-y-2 md:hidden"
        >
          <div
            v-for="record in records"
            :key="record.recordId"
            class="flex items-center gap-3 rounded-2xl bg-white px-4 py-3.5 shadow-sm"
          >

            <div
              :class="[
                'flex h-10 w-10 shrink-0 items-center justify-center rounded-xl',
                typeIconClass(record),
              ]"
            >
              <component
                :is="typeIcon(record)"
                class="h-4 w-4"
              />
            </div>

            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-semibold text-slate-900">
                {{ record.transactionCategory }}
              </p>

              <p class="mt-0.5 truncate text-xs text-slate-400">
                {{ record.operator }} · {{ record.date }}
              </p>
            </div>

            <div class="text-right">
              <p
                :class="[
                  'text-sm font-semibold',
                  amountClass(record),
                ]"
              >
                {{ isIncome(record) ? '+' : '-' }}{{ formatCurrency(record.amount) }}
              </p>

              <p class="mt-0.5 text-[10px] text-slate-400">
                {{ record.transactionType }}
              </p>
            </div>

            <button
              @click="openDeleteModal(record.recordId)"
              class="ml-1 rounded-lg p-1.5 text-slate-300 transition hover:bg-rose-50 hover:text-rose-500"
              aria-label="Delete record"
            >
              <Trash2 class="h-4 w-4" />
            </button>

          </div>
        </div>

        <!-- Desktop Transactions -->
        <div
          v-if="records.length > 0"
          class="hidden overflow-hidden rounded-2xl bg-white shadow-sm md:block"
        >
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">

              <thead class="border-b border-slate-100">
                <tr>
                  <th class="px-5 py-4 text-xs font-medium text-slate-400">
                    Transaction
                  </th>

                  <th class="px-5 py-4 text-xs font-medium text-slate-400">
                    Type
                  </th>

                  <th class="px-5 py-4 text-xs font-medium text-slate-400">
                    Date
                  </th>

                  <th class="px-5 py-4 text-xs font-medium text-slate-400">
                    Operator
                  </th>

                  <th
                    class="px-5 py-4 text-right text-xs font-medium text-slate-400"
                  >
                    Amount
                  </th>

                  <th class="w-12 px-4 py-4"></th>
                </tr>
              </thead>

              <tbody class="divide-y divide-slate-50">

                <tr
                  v-for="record in records"
                  :key="record.recordId"
                  class="transition hover:bg-slate-50/60"
                >

                  <td class="px-5 py-4">
                    <div class="flex items-center gap-3">

                      <div
                        :class="[
                          'flex h-9 w-9 items-center justify-center rounded-xl',
                          typeIconClass(record),
                        ]"
                      >
                        <component
                          :is="typeIcon(record)"
                          class="h-4 w-4"
                        />
                      </div>

                      <div>
                        <p class="font-medium text-slate-900">
                          {{ record.transactionCategory }}
                        </p>

                        <p class="mt-0.5 text-xs text-slate-400">
                          {{ record.notes || 'No notes' }}
                        </p>
                      </div>

                    </div>
                  </td>

                  <td class="px-5 py-4">
                    <span
                      :class="[
                        'inline-flex rounded-full px-2.5 py-1 text-xs font-medium',
                        isIncome(record)
                          ? 'bg-emerald-50 text-emerald-700'
                          : isExpense(record)
                          ? 'bg-rose-50 text-rose-700'
                          : 'bg-indigo-50 text-indigo-700',
                      ]"
                    >
                      {{ record.transactionType }}
                    </span>
                  </td>

                  <td class="px-5 py-4 text-slate-500">
                    {{ record.date }}
                  </td>

                  <td class="px-5 py-4 text-slate-500">
                    {{ record.operator }}
                  </td>

                  <td
                    :class="[
                      'px-5 py-4 text-right font-semibold',
                      amountClass(record),
                    ]"
                  >
                    {{ isIncome(record) ? '+' : '-' }}{{ formatCurrency(record.amount) }}
                  </td>

                  <td class="px-4 py-4 text-right">
                    <button
                      @click="openDeleteModal(record.recordId)"
                      class="rounded-lg p-2 text-slate-300 transition hover:bg-rose-50 hover:text-rose-500"
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

      </section>
    </main>

    <!-- Delete Modal -->
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
          v-if="showDeleteModal"
          class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/30 px-4"
          @click.self="closeDeleteModal"
        >
          <div
            class="w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl"
          >

            <div
              class="flex h-11 w-11 items-center justify-center rounded-xl bg-rose-50 text-rose-600"
            >
              <AlertTriangle class="h-5 w-5" />
            </div>

            <h3 class="mt-4 text-lg font-semibold text-slate-900">
              Delete transaction?
            </h3>

            <p class="mt-2 text-sm leading-6 text-slate-500">
              This transaction will be permanently removed.
              This action cannot be undone.
            </p>

            <div class="mt-6 flex justify-end gap-2">

              <button
                @click="closeDeleteModal"
                class="rounded-xl px-4 py-2.5 text-sm font-medium text-slate-500 transition hover:bg-slate-50 hover:text-slate-700"
              >
                Cancel
              </button>

              <button
                @click="confirmDelete"
                :disabled="deleting"
                class="inline-flex items-center gap-2 rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-rose-700 disabled:opacity-60"
              >
                <span
                  v-if="deleting"
                  class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
                ></span>

                {{ deleting ? 'Deleting...' : 'Delete' }}
              </button>

            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>
```