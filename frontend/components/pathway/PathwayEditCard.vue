<template>
    <div v-if="draft" class="mx-auto min-w-full">
        <PathwayHeadingEditPanel :title="pathwayStore.draft.title as string" :approach="saveApproach"
            @set-edit-request="watchEditHeadingRequest" />
        <form class="flex-auto rounded-lg p-3">
            <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
                <div class="col-span-full">
                    <label for="pathway-title" class="block text-sm font-semibold leading-6 text-gray-900">{{
                        t("pathway.field.title") }}</label>
                    <div class="mt-2">
                        <input type="text" name="pathway-title" id="pathway-title" v-model="draft.title"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                    </div>
                    <p v-if="pathwayStore.isTranslatingDraft" class="mt-2 text-sm leading-6 text-gray-500">{{
                        pathwayStore.draft.title }}</p>
                </div>
                <div class="col-span-full">
                    <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">{{
                        t("pathway.field.description") }}</label>
                    <div class="mt-2">
                        <textarea id="description" name="description" rows="3" v-model="draft.description"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
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
                        <input type="text" name="pathway-subject-values" id="pathway-subject-values" v-model="subjects"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                    </div>
                    <p class="mt-2 text-sm leading-6 text-gray-500">{{ t("pathway.help.subjects") }}</p>
                </div>
                <div class="col-span-full">
                    <label for="pathway-spatial-values" class="block text-sm font-semibold leading-6 text-gray-900">
                        {{ t("pathway.field.spatial") }}
                    </label>
                    <div class="mt-2">
                        <input type="text" name="pathway-spatial-values" id="pathway-spatial-values" v-model="draft.spatial"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                    </div>
                    <p class="mt-2 text-sm leading-6 text-gray-500">
                        {{ t("pathway.help.spatial") }}
                    </p>
                </div>
                <div class="col-span-full">
                    <label for="pathway-temporal-values" class="block text-sm font-semibold leading-6 text-gray-900">
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
                    <label for="pathway-language-values" class="block text-sm font-semibold leading-6 text-gray-900">
                        {{ t("pathway.field.language") }}
                    </label>
                    <div class="mt-2">
                        <CommonLocaleDropdown :language="pathwayStore.draft.language as string"
                            @set-locale-select="watchLocaleSelect" />
                        <!-- <input type="text" name="pathway-language-values" id="pathway-language-values"
                            v-model="draft.language"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" /> -->
                    </div>
                    <p class="mt-2 text-sm leading-6 text-gray-500">
                        {{ t("pathway.help.language") }}
                    </p>
                </div>
                <!-- 
                <div class="col-span-full">
                    <label for="pathway-accrual-method-values"
                        class="block text-sm font-semibold leading-6 text-gray-900">Accrual
                        method</label>
                    <div class="mt-2">
                        <Listbox v-model="draft.accrualMethod">
                            <div class="relative mt-1">
                                <ListboxButton
                                    class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-spring-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-spring-300 sm:text-sm">
                                    <span v-if="draft.accrualMethod" class="block truncate">{{
                                        capitalizeFirst(draft.accrualMethod)
                                    }}</span>
                                    <span v-else class="block truncate">Select...</span>
                                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                        <PhCaretUpDown class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                    </span>
                                </ListboxButton>
                                <transition leave-active-class="transition duration-100 ease-in"
                                    leave-from-class="opacity-100" leave-to-class="opacity-0">
                                    <ListboxOptions
                                        class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                        <ListboxOption v-slot="{ active, selected }" v-for="mtype in parameters.accrualType"
                                            :key="`mtype-${mtype.value}`" :value="mtype.value" as="template">
                                            <li :class="[
                                                active ? 'bg-spring-100 text-spring-900' : 'text-gray-900',
                                                'relative cursor-default select-none py-2 pl-10 pr-4',
                                            ]">
                                                <span :class="[
                                                    selected ? 'font-medium' : 'font-normal',
                                                    'block truncate',
                                                ]">{{ capitalizeFirst(mtype.value) }}</span>
                                                <span v-if="selected"
                                                    class="absolute inset-y-0 left-0 flex items-center pl-3 text-spring-600">
                                                    <PhCheck class="h-5 w-5" aria-hidden="true" />
                                                </span>
                                            </li>
                                        </ListboxOption>
                                    </ListboxOptions>
                                </transition>
                            </div>
                        </Listbox>
                    </div>
                    <p class="mt-2 text-sm leading-6 text-gray-600">
                        The method by which items are added to a resource.
                    </p>
                </div> -->
                <div class="col-span-full">
                    <label for="pathway-bibliographic-citation-values"
                        class="block text-sm font-semibold leading-6 text-gray-900">
                        {{ t("pathway.field.citation") }}
                    </label>
                    <div class="mt-2">
                        <input type="text" name="pathway-bibliographic-citation-values"
                            id="pathway-bibliographic-citation-values" v-model="draft.bibliographicCitation"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                    </div>
                    <p class="mt-2 text-sm leading-6 text-gray-500">
                        {{ t("pathway.help.citation") }}
                    </p>
                </div>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, } from "@headlessui/vue"
import { PhCheck, PhCaretUpDown } from "@phosphor-icons/vue"
import { capitalizeFirst } from "@/utilities"
import { IPathway } from "@/interfaces"
import { usePathwayStore } from "@/stores"
import dayjs from "dayjs"

const { t } = useI18n()
const route = useRoute()
const pathwayStore = usePathwayStore()
const draft = ref({} as IPathway)
const saveApproach = ref("Create")
const subjects = ref("")
const dateFrom = ref("")
const dateTo = ref("")
const formatter = ref({
    date: "YYYY-MM-DD",
    month: "MMM"
})

const parameters = {
    accrualPolicyType: [
        { value: "closed" },
        { value: "passive" },
        { value: "active" },
        { value: "partial" },
    ],
    accrualType: [
        { value: "deposit" },
        { value: "donation" },
        { value: "purchase" },
        { value: "loan" },
        { value: "license" },
        { value: "itemCreation" },
    ],
    frequencyType: [
        { value: "triennial" },
        { value: "biennial" },
        { value: "annual" },
        { value: "semiannual" },
        { value: "threeTimesAYear" },
        { value: "quarterly" },
        { value: "bimonthly" },
        { value: "monthly" },
        { value: "semimonthly" },
        { value: "biweekly" },
        { value: "threeTimesAMonth" },
        { value: "weekly" },
        { value: "semiweekly" },
        { value: "threeTimesAWeek" },
        { value: "daily" },
        { value: "continuous" },
        { value: "irregular" },
    ]
}

async function watchEditHeadingRequest(request: string) {
    switch (request) {
        case "reset":
            resetForm()
            break
        case "save":
            submitRequest()
            break
        case "cancel":
            // resetForm()
            if (route.params.id === "create") return await navigateTo("/pathway")
            else return await navigateTo(`/pathway/${route.params.id}`)
    }
}

async function watchLocaleSelect(select: string) {
    draft.value.language = select
    pathwayStore.setLanguageDraft(select)
}

function resetDraft() {
    draft.value = { ...pathwayStore.draft }
    dateFrom.value = ""
    dateTo.value = ""
    if (draft.value.temporalStart) dateFrom.value = draft.value.temporalStart.split("T")[0]
    if (draft.value.temporalEnd) dateTo.value = draft.value.temporalEnd.split("T")[0]
    if (draft.value.subjects && draft.value.subjects.length) subjects.value = draft.value.subjects.join(", ")
}

function resetForm() {
    if (route.params.id === "create") pathwayStore.resetDraft()
    if (saveApproach.value === "Update") pathwayStore.setDraft({ ...pathwayStore.term })
    resetDraft()
}

async function submitRequest() {
    // https://stackoverflow.com/a/38201551/295606
    if (subjects.value) draft.value.subjects = subjects.value.split(",").map((item: string) => item.trim())
    if (dateFrom.value && dateTo.value && dateFrom.value >= dateTo.value) dateTo.value = ""
    if (dateFrom.value) draft.value.temporalStart = dayjs(dateFrom.value).format()
    if (dateTo.value) draft.value.temporalEnd = dayjs(dateTo.value).format()
    pathwayStore.setDraft(draft.value)
    if (saveApproach.value === "Update" && draft.value.id)
        await pathwayStore.updateTerm(draft.value.id)
    else await pathwayStore.createTerm()
    return await navigateTo(`/pathway/${pathwayStore.term.id}`)
}

onMounted(async () => {
    if (route.params.id !== "create") saveApproach.value = "Update"
    if (pathwayStore.draft && Object.keys(pathwayStore.draft).length !== 0) resetDraft()
    else resetForm()
})

onBeforeRouteLeave((to, from, next) => {
    pathwayStore.setDraft(draft.value)
    next()
})
</script>