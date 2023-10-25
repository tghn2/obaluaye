<template>
    <Disclosure as="section" aria-labelledby="filter-heading" class="grid items-center my-2">
        <h2 id="filter-heading" class="sr-only">{{ t("filter.filters") }}</h2>
        <div class="col-start-1 row-start-1 py-4">
            <div class="relative flex justify-between items-center sm:ml-6 px-4 text-xs sm:px-6">
                <div class="items-center flex max-w-7xl space-x-3 divide-x divide-gray-200">
                    <DisclosureButton class="search flex items-center font-medium text-gray-700 hover:text-kashmir-600">
                        <PhFunnel class="mr-2 h-5 w-5 flex-none text-gray-400 search-hover:text-kashmir-600"
                            aria-hidden="true" />
                        {{ t("filter.filters") }}
                    </DisclosureButton>
                    <div class="pl-3">
                        <span class="sr-only">{{ t("filter.clear") }}</span>
                        <button type="button" @click="resetFilters" class="text-gray-500 hover:text-kashmir-600">
                            {{ t("filter.clear") }}
                        </button>
                    </div>
                </div>
                <div class="flex items-center justify-center sm:mx-4 px-2 w-full">
                    <div class="w-full">
                        <label for="search" class="sr-only">{{ t("filter.search") }}</label>
                        <div class="relative">
                            <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                <PhMagnifyingGlass class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </div>
                            <input id="search" name="search" v-model="searchTerm" @keydown="watchSearchTerm"
                                class="block w-full rounded-md border-0 bg-white py-1.5 pl-10 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6"
                                :placeholder="t('filter.search')" type="search" />
                        </div>
                    </div>
                </div>
                <button type="button" @click="refreshSearchs" class="search inline-flex justify-center">
                    <PhArrowsClockwise
                        class="-mr-1 ml-1 mt-1 h-5 w-5 flex-shrink-0 text-gray-400 search-hover:text-kashmir-600"
                        aria-hidden="true" />
                    <span class="sr-only">{{ t("filter.refresh") }}</span>
                </button>
            </div>
        </div>
        <DisclosurePanel class="border-t border-gray-200 py-5 px-8 space-y-4 text-xs sm:text-sm">
            <div class="flex justify-between">
                <fieldset>
                    <legend class="block font-bold pb-4">{{ t("filter.language") }}</legend>
                    <CommonLocaleDropdown :language="filters.language" @set-locale-select="watchLocaleSelect" />
                </fieldset>
                <fieldset>
                    <legend class="block font-bold pb-4">{{ t("filter.complete") }}</legend>
                    <Switch v-model="filters.complete"
                        class="group relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-kashmir-600 focus:ring-offset-2">
                        <span class="sr-only">Use setting</span>
                        <span aria-hidden="true" class="pointer-events-none absolute h-full w-full rounded-md bg-white" />
                        <span aria-hidden="true"
                            :class="[filters.complete ? 'bg-kashmir-600' : 'bg-gray-200', 'pointer-events-none absolute mx-auto h-4 w-9 rounded-full transition-colors duration-200 ease-in-out']" />
                        <span aria-hidden="true"
                            :class="[filters.complete ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none absolute left-0 inline-block h-5 w-5 transform rounded-full border border-gray-200 bg-white shadow ring-0 transition-transform duration-200 ease-in-out']" />
                    </Switch>
                </fieldset>
                <fieldset>
                    <legend class="block font-bold pb-4">{{ t("filter.featured") }}</legend>
                    <Switch v-model="filters.featured"
                        class="group relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-kashmir-600 focus:ring-offset-2">
                        <span class="sr-only">Use setting</span>
                        <span aria-hidden="true" class="pointer-events-none absolute h-full w-full rounded-md bg-white" />
                        <span aria-hidden="true"
                            :class="[filters.featured ? 'bg-kashmir-600' : 'bg-gray-200', 'pointer-events-none absolute mx-auto h-4 w-9 rounded-full transition-colors duration-200 ease-in-out']" />
                        <span aria-hidden="true"
                            :class="[filters.featured ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none absolute left-0 inline-block h-5 w-5 transform rounded-full border border-gray-200 bg-white shadow ring-0 transition-transform duration-200 ease-in-out']" />
                    </Switch>
                </fieldset>
            </div>
            <div class="mx-auto">
                <fieldset>
                    <legend class="block font-bold pb-4">{{ t("filter.dates") }}</legend>
                    <div class="flex space-x-4 items-center">
                        <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateFrom" />
                        <span class="text-gray-600">{{ t("filter.to") }}</span>
                        <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
                    </div>
                </fieldset>
            </div>
            <div class="flex flex-row justify-end pt-4">
                <button type="submit" @click="refreshSearchs"
                    class="w-20 justify-center rounded-md border border-transparent bg-kashmir-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-kashmir-700 focus:outline-none focus:ring-2 focus:ring-kashmir-600 focus:ring-offset-2">
                    {{ t("filter.filter") }}
                </button>
            </div>
        </DisclosurePanel>
    </Disclosure>
</template>

<script setup lang="ts">
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { Disclosure, DisclosureButton, DisclosurePanel, Switch } from "@headlessui/vue"
import {
    PhArrowsClockwise,
    PhMagnifyingGlass,
    PhFunnel,
} from "@phosphor-icons/vue"
import { useSearchStore } from "@/stores"
import { IFilters } from "@/interfaces"

const { t } = useI18n()
const searchStore = useSearchStore()
const filters = ref({} as IFilters)
const searchTerm = ref("")
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
    date: "YYYY-MM-DD",
    month: "MMM"
})

function watchSearchTerm(event: any) {
    if (event.key === "Enter") refreshSearchs()
}

function watchLocaleSelect(response: string) {
    filters.value.language = response
}

async function refreshSearchs() {
    filters.value.match = searchTerm.value
    if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
    if (dateFrom.value) filters.value.date_from = dateFrom.value
    if (dateTo.value) filters.value.date_to = dateTo.value
    searchStore.setFilters(filters.value)
    getFilters()
    await searchStore.getMulti()
}

function getFilters() {
    filters.value = { ...searchStore.filters }
    searchTerm.value = ""
    dateFrom.value = ""
    dateTo.value = ""
    if (filters.value.date_from) dateFrom.value = filters.value.date_from
    if (filters.value.date_to) dateTo.value = filters.value.date_to
    if (filters.value.match) searchTerm.value = filters.value.match
}

async function resetFilters() {
    searchStore.resetFilters()
    getFilters()
    await refreshSearchs()
}

onMounted(async () => {
    getFilters()
})

</script>