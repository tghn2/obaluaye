<template>
    <div class="p-2 border-b-2 border-kashmir-100">
        <Disclosure v-slot="{ open, close }">
            <DisclosureButton @click="disclosureWatcher(open, close)"
                class="flex w-full justify-between items-center rounded-lg text-base font-semibold text-gray-900 px-2">
                <h1 v-if="draft.title">{{ draft.title }}</h1>
                <h1 v-else class="text-gray-700 italic">{{ t("pathway.new") }}</h1>
                <PhCaretDown :class="open ? 'rotate-180 transform' : ''" class="h-5 w-5" />
            </DisclosureButton>
            <DisclosurePanel class="px-4 text-sm text-gray-500">
                <form class="flex-auto rounded-lg p-3">
                    <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
                        <div class="sm:col-span-4">
                            <label for="pathway-title" class="block text-sm font-semibold leading-6 text-gray-900">{{
                                t("pathway.field.title") }}</label>
                            <div class="mt-2">
                                <input type="text" name="pathway-title" id="pathway-title" v-model="draft.title"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p v-if="pathwayStore.isTranslatingDraft" class="mt-2 text-sm leading-6 text-gray-500">
                                {{ pathwayStore.draft.title }}
                            </p>
                        </div>
                        <div class="sm:col-span-2">
                            <label for="pathway-type" class="block text-sm font-semibold leading-6 text-gray-900">{{
                                t("pathway.field.type") }}</label>
                            <div class="mt-2">
                                <InputSelectPathType name="pathway-type" id="pathway-type"
                                    :initial-type="pathwayStore.draft.pathType" @set-select="watchInputPathType" />
                            </div>
                        </div>
                        <div class="col-span-full">
                            <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">{{
                                t("pathway.field.description") }}</label>
                            <div class="mt-2">
                                <textarea id="description" name="description" rows="3" v-model="draft.description"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">
                                <span v-if="pathwayStore.isTranslatingDraft">{{ pathwayStore.draft.description }}</span>
                                <span v-else>{{ t("pathway.help.description") }}</span>
                            </p>
                        </div>
                        <div class="col-span-full">
                            <label for="pathway-subject-values" class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ t("pathway.field.subjects") }}
                            </label>
                            <div class="mt-2">
                                <input type="text" name="pathway-subject-values" id="pathway-subject-values"
                                    v-model="subjects"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">{{ t("pathway.help.subjects") }}</p>
                        </div>
                        <div class="col-span-full">
                            <label for="pathway-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ t("pathway.field.country") }}
                            </label>
                            <div class="mt-2">
                                <CommonCountrySelect :initial-choices="draft.country" @set-select="watchCountrySelect" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">
                                {{ t("pathway.help.country") }}
                            </p>
                        </div>
                        <div class="col-span-full">
                            <label for="pathway-spatial-values" class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ t("pathway.field.spatial") }}
                            </label>
                            <div class="mt-2">
                                <input type="text" name="pathway-spatial-values" id="pathway-spatial-values"
                                    v-model="draft.spatial"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">
                                {{ t("pathway.help.spatial") }}
                            </p>
                        </div>
                        <div class="col-span-full">
                            <label for="pathway-temporal-values"
                                class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ t("pathway.field.temporal") }}
                            </label>
                            <div class="mt-2">
                                <div class="flex space-x-4 items-center">
                                    <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateFrom" />
                                    <span class="text-gray-600">to</span>
                                    <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
                                </div>
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">
                                {{ t("pathway.help.temporal") }}
                            </p>
                        </div>
                        <div class="col-span-full">
                            <label for="pathway-bibliographic-citation-values"
                                class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ t("pathway.field.citation") }}
                            </label>
                            <div class="mt-2">
                                <input type="text" name="pathway-bibliographic-citation-values"
                                    id="pathway-bibliographic-citation-values" v-model="draft.bibliographicCitation"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">
                                {{ t("pathway.help.citation") }}
                            </p>
                        </div>
                        <div class="col-span-full my-1 py-1 border-t border-gray-100">
                            <PathwayEditResourceCard :initial-drafts="draft.resources" @set-drafts="watchResourcesUpdate" />
                        </div>
                    </div>
                </form>
            </DisclosurePanel>
        </Disclosure>
    </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia"
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { PhCaretDown } from "@phosphor-icons/vue"
import { IPathway, IPathwayType, IResource } from "@/interfaces"
import { usePathwayStore } from "@/stores"
import dayjs from "dayjs"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const { activeEdit, languageEdit } = storeToRefs(pathwayStore)
const toggleClose = ref({} as typeof ref | HTMLElement)
const openState = ref(false)
const draft = ref({} as IPathway)
const subjects = ref("")
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
    date: "YYYY-MM-DD",
    month: "MMM"
})

const props = defineProps<{
    initialDraft: IPathway,
}>()
const emit = defineEmits<{
    setDraft: [draft: IPathway],
}>()

// WATCHERS
function disclosureWatcher(open: boolean, close: typeof ref | HTMLElement) {
    // `open` seems to be false if open and true of closed ...
    if (!open) {
        toggleClose.value = close
        openState.value = true
        pathwayStore.setActiveDraft(props.initialDraft.id as string)
    } else {
        openState.value = false
        pathwayStore.setActiveDraft("")
    }
}

function watchCountrySelect(response: string[]) {
    draft.value.country = response
}

function watchInputPathType(response: IPathwayType) {
    draft.value.pathType = response
}

function watchResourcesUpdate(update: IResource[]) {
    // console.log("watchResourcesUpdate", update)
    draft.value.resources = update
}

watch(() => pathwayStore.activeEdit, () => {
    // @ts-ignore
    if (openState.value && props.initialDraft.id !== pathwayStore.activeDraft) toggleClose.value()
})

watch(
    () => [draft.value, subjects.value], () => {
        const response = setDraft({ ...draft.value })
        emit("setDraft", response)
    },
    { deep: true }
)

// SETTERS
function setDraft(response: IPathway) {
    // https://stackoverflow.com/a/38201551/295606
    if (subjects.value) response.subjects = subjects.value.split(",").map((item: string) => item.trim())
    else response.subjects = [] as string[]
    if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
    if (dateFrom.value) response.temporalStart = dayjs(dateFrom.value).format()
    if (dateTo.value) response.temporalEnd = dayjs(dateTo.value).format()
    return response
}

function resetDraft() {
    draft.value = { ...props.initialDraft }
    dateFrom.value = ""
    dateTo.value = ""
    if (draft.value.temporalStart) dateFrom.value = draft.value.temporalStart.split("T")[0]
    if (draft.value.temporalEnd) dateTo.value = draft.value.temporalEnd.split("T")[0]
    if (draft.value.subjects && draft.value.subjects.length) subjects.value = draft.value.subjects.join(", ")
}

onMounted(async () => {
    resetDraft()
})
</script>