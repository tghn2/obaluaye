<template>
    <Disclosure as="section" aria-labelledby="filter-heading" class="grid items-center my-2">
        <h2 id="filter-heading" class="sr-only">{{ t("filter.filters") }}</h2>
        <div class="col-start-1 row-start-1 py-4">
            <div class="relative flex justify-between items-center sm:ml-6 px-4 text-xs sm:px-6">
                <div class="items-center flex max-w-7xl space-x-3 divide-x divide-gray-200">
                    <DisclosureButton class="comment flex items-center font-medium text-gray-700 hover:text-kashmir-600">
                        <PhFunnel class="mr-2 h-5 w-5 flex-none text-gray-400 comment-hover:text-kashmir-600"
                            aria-hidden="true" />
                        {{ t("filter.filters") }}
                    </DisclosureButton>
                    <div class="pl-3">
                        <span class="sr-only">{{ t("filter.clear") }}</span>
                        <button type="button" @click="resetFilters"
                            class="text-gray-500 hover:text-kashmir-600">Clear</button>
                    </div>
                </div>
                <button type="button" @click="refreshComments" class="comment inline-flex justify-center">
                    <PhArrowsClockwise
                        class="-mr-1 ml-1 mt-1 h-5 w-5 flex-shrink-0 text-gray-400 comment-hover:text-kashmir-600"
                        aria-hidden="true" />
                    <span class="sr-only">{{ t("filter.refresh") }}</span>
                </button>
            </div>
        </div>
        <DisclosurePanel class="border-t border-gray-200 py-5">
            <div class="mx-auto text-xs sm:text-sm px-8 space-y-4">
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
                <button type="submit" @click="refreshComments"
                    class="w-20 justify-center rounded-md border border-transparent bg-kashmir-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-kashmir-700 focus:outline-none focus:ring-2 focus:ring-kashmir-600 focus:ring-offset-2">
                    {{ t("filter.filter") }}
                </button>
            </div>
        </DisclosurePanel>
    </Disclosure>
</template>

<script setup lang="ts">
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import {
    PhArrowsClockwise,
    PhFunnel,
} from "@phosphor-icons/vue"
import { useCommentStore } from "@/stores"
import { IFilters } from "@/interfaces"

const { t } = useI18n()
const commentStore = useCommentStore()
const filters = ref({} as IFilters)
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
    date: "YYYY-MM-DD",
    month: "MMM"
})

async function refreshComments() {
    if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
    if (dateFrom.value) filters.value.date_from = dateFrom.value
    if (dateTo.value) filters.value.date_to = dateTo.value
    commentStore.setFilters(filters.value)
    getFilters()
    await commentStore.getMulti()
}

function getFilters() {
    filters.value = { ...commentStore.filters }
    dateFrom.value = ""
    dateTo.value = ""
    if (filters.value.date_from) dateFrom.value = filters.value.date_from
    if (filters.value.date_to) dateTo.value = filters.value.date_to
}

async function resetFilters() {
    commentStore.resetFilters()
    getFilters()
    await refreshComments()
}

onMounted(async () => {
    getFilters()
})

</script>