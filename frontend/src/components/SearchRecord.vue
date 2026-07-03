<script setup lang="ts">
import { ref } from 'vue';
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
  Search,
  X,
  ChevronDown,
  FileText,
  Fingerprint,
  TrendingUp,
  Tag,
} from '@lucide/vue';

type SearchMode = 'id' | 'type' | 'category';

const isOpen = ref(false);
const mode = ref<SearchMode>('id');
const query = ref('');
const loading = ref(false);
const error = ref<string | null>(null);
const results = ref<RecordItem[]>([]);
const searched = ref(false);

const modeOptions: { key: SearchMode; label: string; icon: typeof Fingerprint }[] = [
  { key: 'id', label: 'Record ID', icon: Fingerprint },
  { key: 'type', label: 'Transaction Type', icon: TrendingUp },
  { key: 'category', label: 'Category', icon: Tag },
];

function open() {
  isOpen.value = true;
  reset();
}

function close() {
  isOpen.value = false;
}

function reset() {
  mode.value = 'id';
  query.value = '';
  error.value = null;
  results.value = [];
  searched.value = false;
}

async function submit() {
  if (!query.value.trim()) {
    error.value = 'Please enter a search value';
    return;
  }

  loading.value = true;
  error.value = null;
  results.value = [];
  searched.value = true;

  try {
    if (mode.value === 'id') {
      const record = await recordApi.getById(query.value.trim());
      results.value = record ? [record] : [];
    } else if (mode.value === 'type') {
      results.value = await recordApi.getByType(query.value as TransactionType);
    } else if (mode.value === 'category') {
      results.value = await recordApi.getByCategory(query.value as TransactionCategory);
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Search failed';
  } finally {
    loading.value = false;
  }
}

function setMode(newMode: SearchMode) {
  mode.value = newMode;
  query.value = '';
  error.value = null;
  results.value = [];
  searched.value = false;
}
</script>

<template>
  <div>
    <button
      @click="open"
      class="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-700 shadow-sm ring-1 ring-slate-200 transition-all hover:bg-slate-50 hover:text-indigo-600 hover:ring-indigo-200 active:translate-y-0"
    >
      <Search class="h-4 w-4" />
      Search
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
                  <h2 class="text-lg font-semibold text-slate-900">Search Records</h2>
                  <p class="text-sm text-slate-500">Find records by ID, type, or category</p>
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
                <div v-if="error" class="mb-5 rounded-xl bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
                  {{ error }}
                </div>

                <div class="mb-5 space-y-1.5">
                  <label class="text-sm font-medium text-slate-700">Search By</label>
                  <div class="grid grid-cols-1 gap-2 sm:grid-cols-3">
                    <button
                      v-for="option in modeOptions"
                      :key="option.key"
                      type="button"
                      @click="setMode(option.key)"
                      :class="[
                        'flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium transition-all',
                        mode === option.key
                          ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200'
                          : 'bg-slate-50 text-slate-600 ring-1 ring-slate-200 hover:bg-slate-100',
                      ]"
                    >
                      <component :is="option.icon" class="h-4 w-4" />
                      {{ option.label }}
                    </button>
                  </div>
                </div>

                <div class="space-y-1.5">
                  <label class="text-sm font-medium text-slate-700">{{ modeOptions.find((m) => m.key === mode)?.label }}</label>

                  <div v-if="mode === 'id'">
                    <input
                      v-model="query"
                      type="text"
                      placeholder="e.g. rec-001"
                      class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 px-4 text-sm text-slate-900 outline-none transition-all placeholder:text-slate-400 focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                    />
                  </div>

                  <div v-else-if="mode === 'type'" class="relative">
                    <select
                      v-model="query"
                      class="w-full appearance-none rounded-xl border border-slate-200 bg-slate-50 py-3 pl-4 pr-10 text-sm text-slate-900 outline-none transition-all focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                    >
                      <option value="" disabled>Select a transaction type</option>
                      <option v-for="type in TRANSACTION_TYPES" :key="type" :value="type">{{ type }}</option>
                    </select>
                    <div class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                      <ChevronDown class="h-4 w-4" />
                    </div>
                  </div>

                  <div v-else-if="mode === 'category'" class="relative">
                    <select
                      v-model="query"
                      class="w-full appearance-none rounded-xl border border-slate-200 bg-slate-50 py-3 pl-4 pr-10 text-sm text-slate-900 outline-none transition-all focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                    >
                      <option value="" disabled>Select a category</option>
                      <option v-for="category in TRANSACTION_CATEGORIES" :key="category" :value="category">
                        {{ getTransactionCategoryLabel(category) }}
                      </option>
                    </select>
                    <div class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                      <ChevronDown class="h-4 w-4" />
                    </div>
                  </div>
                </div>

                <div class="mt-6 flex items-center justify-end gap-3">
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
                    class="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white shadow-md shadow-indigo-200 transition-all hover:bg-indigo-700 disabled:opacity-60"
                  >
                    <span v-if="loading" class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
                    <Search v-else class="h-4 w-4" />
                    {{ loading ? 'Searching...' : 'Search' }}
                  </button>
                </div>
              </form>

              <div v-if="searched && !loading" class="border-t border-slate-100 px-6 py-6">
                <h3 class="mb-3 text-sm font-semibold text-slate-700">Search Results ({{ results.length }})</h3>

                <div v-if="results.length === 0" class="rounded-xl bg-slate-50 py-10 text-center">
                  <FileText class="mx-auto mb-3 h-8 w-8 text-slate-300" />
                  <p class="text-sm text-slate-500">No records found for your search.</p>
                </div>

                <div v-else class="space-y-3">
                  <div
                    v-for="record in results"
                    :key="record.recordId"
                    class="rounded-xl border border-slate-100 bg-slate-50 p-4"
                  >
                    <div class="flex flex-wrap items-center justify-between gap-2">
                      <span class="font-semibold text-slate-900">{{ record.recordId }}</span>
                      <span
                        :class="[
                          'inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium',
                          record.transactionType === TransactionType.INCOME
                            ? 'bg-emerald-100 text-emerald-700'
                            : record.transactionType === TransactionType.EXPENSE
                            ? 'bg-rose-100 text-rose-700'
                            : 'bg-indigo-100 text-indigo-700',
                        ]"
                      >
                        {{ record.transactionType }}
                      </span>
                    </div>
                    <div class="mt-2 grid grid-cols-2 gap-2 text-sm text-slate-600">
                      <div><span class="text-slate-400">Amount:</span> ${{ record.amount }}</div>
                      <div><span class="text-slate-400">Category:</span> {{ record.transactionCategory }}</div>
                      <div><span class="text-slate-400">Date:</span> {{ record.date }}</div>
                      <div><span class="text-slate-400">Operator:</span> {{ record.operator }}</div>
                    </div>
                    <div v-if="record.notes" class="mt-2 text-sm text-slate-500">
                      <span class="text-slate-400">Notes:</span> {{ record.notes }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
