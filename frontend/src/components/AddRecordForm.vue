<script setup lang="ts">
import { reactive, ref } from 'vue';
import { recordApi } from '../services/recordApi';
import {
  TransactionType,
  TransactionCategory,
  TRANSACTION_TYPES,
  TRANSACTION_CATEGORIES,
  getTransactionCategoryLabel,
  type RecordItem,
} from '../types/Records';
import {
  Plus,
  X,
  TrendingUp,
  TrendingDown,
  ArrowLeftRight,
  DollarSign,
  CalendarDays,
  User,
  FileText,
  Check,
} from '@lucide/vue';

const emit = defineEmits<{
  added: [];
}>();

const isOpen = ref(false);
const loading = ref(false);
const error = ref<string | null>(null);
const success = ref(false);

const typeMeta: Record<
  TransactionType,
  { label: string; icon: typeof TrendingUp; color: string; activeRing: string; bg: string }
> = {
  [TransactionType.INCOME]: {
    label: 'Income',
    icon: TrendingUp,
    color: 'text-emerald-600',
    activeRing: 'ring-emerald-200',
    bg: 'bg-emerald-50',
  },
  [TransactionType.EXPENSE]: {
    label: 'Expense',
    icon: TrendingDown,
    color: 'text-rose-600',
    activeRing: 'ring-rose-200',
    bg: 'bg-rose-50',
  },
  [TransactionType.TRANSFER]: {
    label: 'Transfer',
    icon: ArrowLeftRight,
    color: 'text-indigo-600',
    activeRing: 'ring-indigo-200',
    bg: 'bg-indigo-50',
  },
};

const form = reactive<RecordItem>({
  recordId: '',
  transactionType: TransactionType.INCOME,
  amount: 0,
  transactionCategory: TransactionCategory.SALARY,
  date: '',
  operator: '',
  notes: '',
});

function open() {
  isOpen.value = true;
  resetForm();
  error.value = null;
  success.value = false;
}

function close() {
  isOpen.value = false;
}

function resetForm() {
  form.recordId = '';
  form.transactionType = TransactionType.INCOME;
  form.amount = 0;
  form.transactionCategory = TransactionCategory.SALARY;
  form.date = '';
  form.operator = '';
  form.notes = '';
}

async function submit() {
  if (!form.recordId.trim()) {
    error.value = 'Please enter a record ID';
    return;
  }
  if (form.amount <= 0) {
    error.value = 'Amount must be greater than zero';
    return;
  }

  loading.value = true;
  error.value = null;
  success.value = false;

  try {
    await recordApi.create({ ...form });
    success.value = true;
    emit('added');
    setTimeout(() => {
      close();
    }, 800);
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to create record';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div>
    <button
      @click="open"
      class="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-200 transition-all hover:bg-indigo-700 hover:shadow-indigo-300 hover:-translate-y-0.5 active:translate-y-0"
    >
      <Plus class="h-5 w-5" />
      Add Record
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
              class="w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl bg-white shadow-2xl ring-1 ring-slate-900/5"
            >
              <div class="flex items-center justify-between border-b border-slate-100 px-6 py-4">
                <div>
                  <h2 class="text-lg font-semibold text-slate-900">Add New Record</h2>
                  <p class="text-sm text-slate-500">Enter the details of your transaction</p>
                </div>
                <button
                  @click="close"
                  class="rounded-lg p-2 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600"
                  aria-label="Close"
                >
                  <X class="h-5 w-5" />
                </button>
              </div>

              <form @submit.prevent="submit" class="p-6">
                <div v-if="success" class="mb-5 flex items-center gap-2 rounded-xl bg-emerald-50 px-4 py-3 text-emerald-700">
                  <Check class="h-5 w-5" />
                  <span class="text-sm font-medium">Record created successfully</span>
                </div>

                <div v-if="error" class="mb-5 rounded-xl bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
                  {{ error }}
                </div>

                <div class="space-y-5">
                  <div class="grid gap-5 sm:grid-cols-2">
                    <div class="space-y-1.5">
                      <label class="text-sm font-medium text-slate-700">Record ID</label>
                      <div class="relative">
                        <FileText class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
                        <input
                          v-model="form.recordId"
                          type="text"
                          placeholder="e.g. rec-001"
                          class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm text-slate-900 outline-none transition-all placeholder:text-slate-400 focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                        />
                      </div>
                    </div>

                    <div class="space-y-1.5">
                      <label class="text-sm font-medium text-slate-700">Amount</label>
                      <div class="relative">
                        <DollarSign class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
                        <input
                          v-model.number="form.amount"
                          type="number"
                          min="1"
                          placeholder="0.00"
                          class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm text-slate-900 outline-none transition-all placeholder:text-slate-400 focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                        />
                      </div>
                    </div>

                    <div class="space-y-1.5">
                      <label class="text-sm font-medium text-slate-700">Date</label>
                      <div class="relative">
                        <CalendarDays class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
                        <input
                          v-model="form.date"
                          type="date"
                          class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm text-slate-900 outline-none transition-all focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                        />
                      </div>
                    </div>

                    <div class="space-y-1.5">
                      <label class="text-sm font-medium text-slate-700">Operator</label>
                      <div class="relative">
                        <User class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
                        <input
                          v-model="form.operator"
                          type="text"
                          placeholder="e.g. admin"
                          class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm text-slate-900 outline-none transition-all placeholder:text-slate-400 focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                        />
                      </div>
                    </div>
                  </div>

                  <div class="space-y-1.5">
                    <label class="text-sm font-medium text-slate-700">Transaction Type</label>
                    <div class="grid grid-cols-3 gap-2 rounded-xl bg-slate-100 p-1.5">
                      <button
                        v-for="type in TRANSACTION_TYPES"
                        :key="type"
                        type="button"
                        @click="form.transactionType = type"
                        :class="[
                          'flex items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium transition-all',
                          form.transactionType === type
                            ? `bg-white shadow-sm ring-1 ${typeMeta[type].activeRing} ${typeMeta[type].color}`
                            : 'text-slate-500 hover:bg-white/60 hover:text-slate-700',
                        ]"
                      >
                        <component
                          :is="typeMeta[type].icon"
                          class="h-4 w-4"
                          :class="form.transactionType === type ? typeMeta[type].color : 'text-slate-400'"
                        />
                        {{ typeMeta[type].label }}
                      </button>
                    </div>
                  </div>

                  <div class="grid gap-5 sm:grid-cols-2">
                    <div class="space-y-1.5">
                      <label class="text-sm font-medium text-slate-700">Category</label>
                      <div class="relative">
                        <select
                          v-model="form.transactionCategory"
                          class="w-full appearance-none rounded-xl border border-slate-200 bg-slate-50 py-3 pl-4 pr-10 text-sm text-slate-900 outline-none transition-all focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                        >
                          <option
                            v-for="category in TRANSACTION_CATEGORIES"
                            :key="category"
                            :value="category"
                          >
                            {{ getTransactionCategoryLabel(category) }}
                          </option>
                        </select>
                        <div class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                          </svg>
                        </div>
                      </div>
                    </div>

                    <div class="space-y-1.5">
                      <label class="text-sm font-medium text-slate-700">Notes</label>
                      <input
                        v-model="form.notes"
                        type="text"
                        placeholder="Optional note"
                        class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 px-4 text-sm text-slate-900 outline-none transition-all placeholder:text-slate-400 focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                      />
                    </div>
                  </div>
                </div>

                <div class="mt-7 flex items-center justify-end gap-3 border-t border-slate-100 pt-5">
                  <button
                    type="button"
                    @click="close"
                    class="rounded-xl px-5 py-2.5 text-sm font-semibold text-slate-600 transition-colors hover:bg-slate-100"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    :disabled="loading"
                    class="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white shadow-md shadow-indigo-200 transition-all hover:bg-indigo-700 hover:shadow-lg active:translate-y-0.5 disabled:opacity-60 disabled:cursor-not-allowed"
                  >
                    <Check v-if="!loading" class="h-4 w-4" />
                    <span v-if="loading" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                    {{ loading ? 'Saving...' : 'Save Record' }}
                  </button>
                </div>
              </form>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
