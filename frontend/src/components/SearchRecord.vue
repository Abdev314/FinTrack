<script setup lang="ts">
import { ref, computed } from 'vue';
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
  CalendarDays,
  User,
} from '@lucide/vue';

type SearchMode = 'id' | 'type' | 'category';

const isOpen = ref(false);
const mode = ref<SearchMode>('id');
const query = ref('');
const loading = ref(false);
const error = ref<string | null>(null);
const results = ref<RecordItem[]>([]);
const searched = ref(false);

const modeOptions = [
  {
    key: 'id' as SearchMode,
    label: 'Record ID',
    icon: Fingerprint,
  },
  {
    key: 'type' as SearchMode,
    label: 'Type',
    icon: TrendingUp,
  },
  {
    key: 'category' as SearchMode,
    label: 'Category',
    icon: Tag,
  },
];

const currentModeLabel = computed(
  () => modeOptions.find((item) => item.key === mode.value)?.label
);

function open() {
  reset();
  isOpen.value = true;
}

function close() {
  if (!loading.value) {
    isOpen.value = false;
  }
}

function reset() {
  mode.value = 'id';
  query.value = '';
  error.value = null;
  results.value = [];
  searched.value = false;
}

function setMode(newMode: SearchMode) {
  mode.value = newMode;
  query.value = '';
  error.value = null;
  results.value = [];
  searched.value = false;
}

async function submit() {
  if (!query.value.trim()) {
    error.value = 'Please select or enter a search value';
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
    }

    if (mode.value === 'type') {
      results.value = await recordApi.getByType(
        query.value as TransactionType
      );
    }

    if (mode.value === 'category') {
      results.value = await recordApi.getByCategory(
        query.value as TransactionCategory
      );
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Search failed';
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

function typeClass(type: TransactionType) {
  if (type === TransactionType.INCOME) {
    return 'bg-emerald-50 text-emerald-700';
  }

  if (type === TransactionType.EXPENSE) {
    return 'bg-rose-50 text-rose-700';
  }

  return 'bg-indigo-50 text-indigo-700';
}
</script>

<template>
  <div>
    <button
      type="button"
      @click="open"
      class="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm ring-1 ring-slate-100 transition-colors hover:bg-slate-50 hover:text-indigo-600"
    >
      <Search class="h-4 w-4" />
      <span>Search</span>
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
                  Search Records
                </h2>
                <p class="mt-0.5 text-sm text-slate-500">
                  Find records by ID, type, or category
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

            <form
              @submit.prevent="submit"
              class="max-h-[calc(100vh-8rem)] overflow-y-auto"
            >
              <div class="space-y-5 p-5 sm:p-6">
                <div
                  v-if="error"
                  class="rounded-xl bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700"
                >
                  {{ error }}
                </div>

                <!-- Search mode -->
                <div>
                  <label class="mb-2 block text-sm font-medium text-slate-700">
                    Search by
                  </label>

                  <div class="grid grid-cols-3 gap-1.5 rounded-xl bg-slate-50 p-1.5">
                    <button
                      v-for="option in modeOptions"
                      :key="option.key"
                      type="button"
                      @click="setMode(option.key)"
                      :class="[
                        'flex items-center justify-center gap-2 rounded-lg px-2 py-2.5 text-sm font-medium transition-colors',
                        mode === option.key
                          ? 'bg-white text-indigo-600 shadow-sm'
                          : 'text-slate-500 hover:bg-white/70 hover:text-slate-700',
                      ]"
                    >
                      <component :is="option.icon" class="h-4 w-4" />

                      <span class="hidden sm:inline">
                        {{ option.label }}
                      </span>
                    </button>
                  </div>
                </div>

                <!-- Query -->
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-slate-700">
                    {{ currentModeLabel }}
                  </label>

                  <div v-if="mode === 'id'">
                    <input
                      v-model="query"
                      type="text"
                      placeholder="Enter record ID"
                      class="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition-colors placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10"
                    />
                  </div>

                  <div v-else class="relative">
                    <select
                      v-model="query"
                      class="w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-3 pr-10 text-sm text-slate-900 outline-none transition-colors focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10"
                    >
                      <option value="" disabled>
                        Select {{ mode === 'type' ? 'a transaction type' : 'a category' }}
                      </option>

                      <template v-if="mode === 'type'">
                        <option
                          v-for="type in TRANSACTION_TYPES"
                          :key="type"
                          :value="type"
                        >
                          {{ type }}
                        </option>
                      </template>

                      <template v-else>
                        <option
                          v-for="category in TRANSACTION_CATEGORIES"
                          :key="category"
                          :value="category"
                        >
                          {{ getTransactionCategoryLabel(category) }}
                        </option>
                      </template>
                    </select>

                    <ChevronDown
                      class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
                    />
                  </div>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex flex-col-reverse gap-2 border-t border-slate-100 px-5 py-4 sm:flex-row sm:justify-end sm:px-6">
                <button
                  type="button"
                  @click="close"
                  class="rounded-xl px-5 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  :disabled="loading"
                  class="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  <span
                    v-if="loading"
                    class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
                  />

                  <Search v-else class="h-4 w-4" />

                  {{ loading ? 'Searching...' : 'Search' }}
                </button>
              </div>
            </form>

            <!-- Results -->
            <div
              v-if="searched && !loading"
              class="border-t border-slate-100 px-5 py-5 sm:px-6"
            >
              <div class="mb-4 flex items-center justify-between">
                <h3 class="text-sm font-semibold text-slate-900">
                  Search Results
                </h3>

                <span class="text-xs text-slate-400">
                  {{ results.length }}
                  {{ results.length === 1 ? 'record' : 'records' }}
                </span>
              </div>

              <div
                v-if="results.length === 0"
                class="rounded-xl bg-slate-50 px-4 py-10 text-center"
              >
                <FileText class="mx-auto h-8 w-8 text-slate-300" />

                <p class="mt-3 text-sm font-medium text-slate-700">
                  No records found
                </p>

                <p class="mt-1 text-xs text-slate-400">
                  Try another search value.
                </p>
              </div>

              <div v-else class="space-y-3">
                <article
                  v-for="record in results"
                  :key="record.recordId"
                  class="rounded-xl bg-white p-4 shadow-sm ring-1 ring-slate-100"
                >
                  <div class="flex items-start justify-between gap-3">
                    <div class="min-w-0">
                      <p class="truncate text-sm font-semibold text-slate-900">
                        {{ record.recordId }}
                      </p>

                      <p class="mt-1 text-sm text-slate-500">
                        {{ record.transactionCategory }}
                      </p>
                    </div>

                    <span
                      :class="[
                        'shrink-0 rounded-full px-2.5 py-1 text-xs font-medium',
                        typeClass(record.transactionType),
                      ]"
                    >
                      {{ record.transactionType }}
                    </span>
                  </div>

                  <p class="mt-4 text-xl font-semibold text-slate-900">
                    {{ formatCurrency(record.amount) }}
                  </p>

                  <div class="mt-4 grid grid-cols-2 gap-3 text-xs">
                    <div>
                      <div class="flex items-center gap-1.5 text-slate-400">
                        <CalendarDays class="h-3.5 w-3.5" />
                        Date
                      </div>
                      <p class="mt-1 text-slate-700">{{ record.date }}</p>
                    </div>

                    <div>
                      <div class="flex items-center gap-1.5 text-slate-400">
                        <User class="h-3.5 w-3.5" />
                        Operator
                      </div>
                      <p class="mt-1 truncate text-slate-700">
                        {{ record.operator }}
                      </p>
                    </div>
                  </div>

                  <p
                    v-if="record.notes"
                    class="mt-4 border-t border-slate-100 pt-3 text-sm text-slate-500"
                  >
                    {{ record.notes }}
                  </p>
                </article>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>