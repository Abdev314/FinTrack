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
  ChevronDown,
} from '@lucide/vue';

const emit = defineEmits<{
  added: [];
}>();

const isOpen = ref(false);
const saving = ref(false);
const error = ref<string | null>(null);
const success = ref(false);

const typeMeta: Record<
  TransactionType,
  {
    label: string;
    icon: typeof TrendingUp;
    color: string;
    bg: string;
    ring: string;
  }
> = {
  [TransactionType.INCOME]: {
    label: 'Income',
    icon: TrendingUp,
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
    ring: 'ring-emerald-200',
  },
  [TransactionType.EXPENSE]: {
    label: 'Expense',
    icon: TrendingDown,
    color: 'text-rose-600',
    bg: 'bg-rose-50',
    ring: 'ring-rose-200',
  },
  [TransactionType.TRANSFER]: {
    label: 'Transfer',
    icon: ArrowLeftRight,
    color: 'text-indigo-600',
    bg: 'bg-indigo-50',
    ring: 'ring-indigo-200',
  },
};

const form = reactive<RecordItem>({
  recordId: '',
  transactionType: TransactionType.INCOME,
  amount: 0,
  transactionCategory: TransactionCategory.SALARY,
  date: new Date().toISOString().split('T')[0],
  operator: '',
  notes: '',
});

function resetForm() {
  Object.assign(form, {
    recordId: '',
    transactionType: TransactionType.INCOME,
    amount: 0,
    transactionCategory: TransactionCategory.SALARY,
    date: new Date().toISOString().split('T')[0],
    operator: '',
    notes: '',
  });

  error.value = null;
  success.value = false;
}

function open() {
  resetForm();
  isOpen.value = true;
}

function close() {
  if (saving.value) return;
  isOpen.value = false;
}

async function submit() {
  error.value = null;
  success.value = false;

  if (!form.amount || form.amount <= 0) {
    error.value = 'Amount must be greater than zero';
    return;
  }

  if (!form.date) {
    error.value = 'Please select a date';
    return;
  }

  if (!form.operator.trim()) {
    error.value = 'Please enter an operator';
    return;
  }

  saving.value = true;

  try {
    await recordApi.create({
      ...form,
      operator: form.operator.trim(),
      notes: form.notes.trim(),
    });

    success.value = true;
    emit('added');

    setTimeout(() => {
      close();
    }, 700);
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Failed to create record';
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <div>
    <!-- Trigger -->
    <button
      type="button"
      @click="open"
      class="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-indigo-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-300"
    >
      <Plus class="h-4 w-4" />
      Add Record
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
          <Transition
            appear
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="translate-y-2 scale-[0.98] opacity-0"
            enter-to-class="translate-y-0 scale-100 opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="translate-y-0 scale-100 opacity-100"
            leave-to-class="translate-y-2 scale-[0.98] opacity-0"
          >
            <div
              v-if="isOpen"
              class="w-full max-w-2xl overflow-hidden rounded-2xl bg-white shadow-xl"
              role="dialog"
              aria-modal="true"
              aria-labelledby="add-record-title"
            >
              <!-- Header -->
              <div class="flex items-center justify-between border-b border-slate-100 px-5 py-4 sm:px-6">
                <div>
                  <h2
                    id="add-record-title"
                    class="text-lg font-semibold text-slate-900"
                  >
                    Add Record
                  </h2>
                  <p class="mt-0.5 text-sm text-slate-500">
                    Create a new financial transaction
                  </p>
                </div>

                <button
                  type="button"
                  @click="close"
                  :disabled="saving"
                  class="rounded-lg p-2 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600 disabled:cursor-not-allowed disabled:opacity-50"
                  aria-label="Close"
                >
                  <X class="h-5 w-5" />
                </button>
              </div>

              <form
                @submit.prevent="submit"
                class="max-h-[calc(100vh-8rem)] overflow-y-auto"
              >
                <div class="space-y-5 p-5 sm:p-6">
                  <!-- Messages -->
                  <div
                    v-if="success"
                    class="flex items-center gap-2 rounded-xl bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-700"
                  >
                    <Check class="h-4 w-4 shrink-0" />
                    Record added successfully.
                  </div>

                  <div
                    v-if="error"
                    class="rounded-xl bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700"
                    role="alert"
                  >
                    {{ error }}
                  </div>

                  <!-- Transaction type -->
                  <div>
                    <label class="mb-2 block text-sm font-medium text-slate-700">
                      Transaction Type
                    </label>

                    <div class="grid grid-cols-3 gap-2 rounded-xl bg-slate-50 p-1.5">
                      <button
                        v-for="type in TRANSACTION_TYPES"
                        :key="type"
                        type="button"
                        @click="form.transactionType = type"
                        :class="[
                          'flex items-center justify-center gap-2 rounded-lg px-2 py-2.5 text-sm font-medium transition-colors',
                          form.transactionType === type
                            ? 'bg-white text-slate-900 shadow-sm'
                            : 'text-slate-500 hover:bg-white/70 hover:text-slate-700',
                        ]"
                      >
                        <component
                          :is="typeMeta[type].icon"
                          class="h-4 w-4"
                          :class="
                            form.transactionType === type
                              ? typeMeta[type].color
                              : 'text-slate-400'
                          "
                        />

                        <span class="hidden sm:inline">
                          {{ typeMeta[type].label }}
                        </span>
                      </button>
                    </div>
                  </div>

                  <!-- Main fields -->
                  <div class="grid gap-5 sm:grid-cols-2">
                    <!-- Amount -->
                    <div>
                      <label
                        for="record-amount"
                        class="mb-1.5 block text-sm font-medium text-slate-700"
                      >
                        Amount
                      </label>

                      <div class="relative">
                        <DollarSign
                          class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
                        />

                        <input
                          id="record-amount"
                          v-model.number="form.amount"
                          type="number"
                          min="0"
                          step="0.01"
                          placeholder="0.00"
                          required
                          class="w-full rounded-xl border border-slate-200 bg-white py-3 pl-9 pr-4 text-sm text-slate-900 outline-none transition-colors placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10"
                        />
                      </div>
                    </div>

                    <!-- Date -->
                    <div>
                      <label
                        for="record-date"
                        class="mb-1.5 block text-sm font-medium text-slate-700"
                      >
                        Date
                      </label>

                      <div class="relative">
                        <CalendarDays
                          class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
                        />

                        <input
                          id="record-date"
                          v-model="form.date"
                          type="date"
                          required
                          class="w-full rounded-xl border border-slate-200 bg-white py-3 pl-9 pr-4 text-sm text-slate-900 outline-none transition-colors focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10"
                        />
                      </div>
                    </div>

                    <!-- Operator -->
                    <div>
                      <label
                        for="record-operator"
                        class="mb-1.5 block text-sm font-medium text-slate-700"
                      >
                        Operator
                      </label>

                      <div class="relative">
                        <User
                          class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
                        />

                        <input
                          id="record-operator"
                          v-model="form.operator"
                          type="text"
                          placeholder="e.g. admin"
                          required
                          class="w-full rounded-xl border border-slate-200 bg-white py-3 pl-9 pr-4 text-sm text-slate-900 outline-none transition-colors placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10"
                        />
                      </div>
                    </div>

                    <!-- Category -->
                    <div>
                      <label
                        for="record-category"
                        class="mb-1.5 block text-sm font-medium text-slate-700"
                      >
                        Category
                      </label>

                      <div class="relative">
                        <select
                          id="record-category"
                          v-model="form.transactionCategory"
                          required
                          class="w-full appearance-none rounded-xl border border-slate-200 bg-white py-3 pl-4 pr-10 text-sm text-slate-900 outline-none transition-colors focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10"
                        >
                          <option
                            v-for="category in TRANSACTION_CATEGORIES"
                            :key="category"
                            :value="category"
                          >
                            {{ getTransactionCategoryLabel(category) }}
                          </option>
                        </select>

                        <ChevronDown
                          class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
                        />
                      </div>
                    </div>
                  </div>

                  <!-- Notes -->
                  <div>
                    <label
                      for="record-notes"
                      class="mb-1.5 block text-sm font-medium text-slate-700"
                    >
                      Notes
                      <span class="font-normal text-slate-400">(optional)</span>
                    </label>

                    <div class="relative">
                      <FileText
                        class="absolute left-3 top-3 h-4 w-4 text-slate-400"
                      />

                      <input
                        id="record-notes"
                        v-model="form.notes"
                        type="text"
                        placeholder="Add a note about this transaction"
                        class="w-full rounded-xl border border-slate-200 bg-white py-3 pl-9 pr-4 text-sm text-slate-900 outline-none transition-colors placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10"
                      />
                    </div>
                  </div>
                </div>

                <!-- Footer -->
                <div
                  class="flex flex-col-reverse gap-2 border-t border-slate-100 px-5 py-4 sm:flex-row sm:justify-end sm:px-6"
                >
                  <button
                    type="button"
                    @click="close"
                    :disabled="saving"
                    class="rounded-xl px-5 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Cancel
                  </button>

                  <button
                    type="submit"
                    :disabled="saving"
                    class="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    <span
                      v-if="saving"
                      class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
                    />

                    <Check v-else class="h-4 w-4" />

                    {{ saving ? 'Adding...' : 'Add Record' }}
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