<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done' && groupStore.term && groupStore.term.hasOwnProperty('name')">
            <GroupHeadingEditView :title="groupStore.term.title as string" @set-edit-request="watchHeadingRequest" />
            <form class="flex-auto rounded-lg p-3">
                <div class="grid grid-cols-1 gap-x-3 gap-y-4 sm:grid-cols-6 p-3">
                    <div class="sm:col-span-5">
                        <label for="group-title" class="block text-sm font-semibold leading-6 text-gray-900">{{
                            t("group.field.title") }}</label>
                        <div class="mt-2 group relative inline-block w-full">
                            <input type="text" name="group-title" id="group-title" v-model="draft.title"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            <div v-if="!formValidates && !draft.title" 
                                class="absolute top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700">
                                <span>{{ t("formvalidation.required") }}</span>
                            </div>
                        </div>
                    </div>
                    <div class="sm:col-span-1">
                        <label for="group-language-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.language") }}
                        </label>
                        <div class="mt-2">
                            <CommonLocaleDropdown :language="draft.language as string"
                                @set-locale-select="watchLocaleSelect" />
                        </div>
                    </div>
                    <div class="col-span-full">
                        <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">{{
                            t("group.field.description") }}</label>
                        <div class="mt-2 group relative inline-block w-full">
                            <textarea id="description" name="description" rows="3" v-model="draft.description"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            <div v-if="!formValidates && !draft.description" 
                                class="absolute -mt-4 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700">
                                <span>{{ t("formvalidation.required") }}</span>
                            </div>
                        </div>
                        <p class="mt-2 text-sm leading-6 text-gray-500">
                            <span>{{ t("group.help.description") }}</span>
                        </p>
                    </div>
                    <div class="col-span-full">
                        <label for="group-subject-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.subjects") }}
                        </label>
                        <div class="mt-2 group relative inline-block w-full">
                            <input type="text" name="group-subject-values" id="group-subject-values" v-model="subjects"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            <div v-if="!formValidates && !subjects" 
                                class="absolute top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700">
                                <span>{{ t("formvalidation.required") }}</span>
                            </div>
                        </div>
                        <p class="mt-2 text-sm leading-6 text-gray-500">{{ t("group.help.subjects") }}</p>
                    </div>
                    <div class="col-span-full">
                        <label for="group-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.country") }}
                        </label>
                        <div class="mt-2 group relative inline-block w-full">
                            <CommonCountrySelect :initial-choices="draft.country" @set-select="watchCountrySelect" />
                            <div v-if="!formValidates && !(draft.country && draft.country.length)" 
                                class="absolute top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700">
                                <span>{{ t("formvalidation.required") }}</span>
                            </div>
                        </div>
                        <p class="mt-2 text-sm leading-6 text-gray-500">
                            {{ t("group.help.country") }}
                        </p>
                    </div>
                    <div class="col-span-full">
                        <label for="group-spatial-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.spatial") }}
                        </label>
                        <div class="mt-2">
                            <input type="text" name="group-spatial-values" id="group-spatial-values" v-model="draft.spatial"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                        </div>
                        <p class="mt-2 text-sm leading-6 text-gray-500">
                            {{ t("group.help.spatial") }}
                        </p>
                    </div>
                </div>
                <div class="pb-6 text-right">
                    <nav class="flex items-center justify-between mb-14 px-4 sm:px-0">
                        <div class="-mt-px flex w-0 flex-1 justify-end">
                            <div class="flex flex-inline items-center space-x-2">
                                <button v-if="groupStore.term.title" @click.prevent="skipToPathway"
                                    class="group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500">
                                    <span>{{ t("pathway.journey.next") }}</span>
                                    <PhArrowRight class="ml-3 h-5 w-5" aria-hidden="true" />
                                </button>
                                <span v-if="groupStore.term.title" class="block h-5 mt-3 w-px bg-gray-900/10" aria-hidden="true" />
                                <button @click.prevent="watchHeadingRequest('save')"
                                    class="group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500">
                                    <span>{{ t("pathway.journey.saveNext") }}</span>
                                    <PhArrowRight class="ml-3 h-5 w-5" aria-hidden="true" />
                                </button>
                            </div>
                        </div>
                    </nav>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhArrowRight } from "@phosphor-icons/vue"
import { useSettingStore, useGroupStore, useJourneyStore } from "@/stores"
import { IGroup } from "@/interfaces"

definePageMeta({
    middleware: ["authenticated"],
})

const { t } = useI18n()
const localePath = useLocalePath()
const appSettings = useSettingStore()
const route = useRoute()
const groupStore = useGroupStore()
const journeyStore = useJourneyStore()
const draft = ref({} as IGroup)
const subjects = ref("")
const groupTitle = ref("group.creating")
const formValidates = ref(true)

// WATCHERS
async function watchHeadingRequest(request: string) {
    switch (request) {
        case "save":
            saveDraft()
            validateDraft()
            if (formValidates.value) {
                await groupStore.updateTerm(route.params.id as string)
                await skipToPathway()
            }
            break
        case "cancel":
            return await navigateTo(localePath(`/group/${route.params.id}`))
    }
}

function watchCountrySelect(response: string[]) {
    draft.value.country = response
}

async function watchLocaleSelect(response: string) {
    draft.value.language = response
}

async function skipToPathway() {
    await journeyStore.getGroupTerm(groupStore.term.id as string, groupStore.term.id as string, false)
    return await navigateTo(localePath(`/journey/${groupStore.term.id as string}/${journeyStore.term.id}`))
}

watch(
    () => [draft.value, subjects.value], () => {
        if (Object.keys(draft.value).length !== 0) {
            saveDraft()
        }
    },
    { deep: true }
)

// SETTERS
function saveDraft() {
    const temporaryDraft = setDraft({ ...draft.value })
    groupStore.setDraft(temporaryDraft)
}

function setDraft(response: IGroup) {
    // https://stackoverflow.com/a/38201551/295606
    if (subjects.value) response.subjects = subjects.value.split(",").map((item: string) => item.trim())
    else response.subjects = [] as string[]
    return response
}

function resetDraft() {
    draft.value = { ...groupStore.term }
    if (draft.value.subjects && draft.value.subjects.length) subjects.value = draft.value.subjects.join(", ")
}

function createDraft() {
    draft.value = {
        id: route.params.id as string,
        language: groupStore.settings.locale,
    }
}

function validateDraft() {
    formValidates.value = true
    if (
        !draft.value.title
        || !draft.value.description
        || !subjects.value
        || !(draft.value.country && draft.value.country.length)
    ) formValidates.value = false
}

onMounted(async () => {
    appSettings.setPageName("nav.groups")
    appSettings.setPageState("loading")
    await groupStore.getTerm(route.params.id as string, false)
    if (!groupStore.term || Object.keys(groupStore.term).length === 0) {
        // The group doesn't exist, so create a draft ...
        groupStore.setCreateDraft(true)
        createDraft()
    } else {
        groupStore.setCreateDraft(false)
        groupTitle.value = "group.updating"
        resetDraft()
    }
    if (!draft.value.language) draft.value.language = groupStore.settings.locale
    groupStore.settings.setPageState("done")
})

// METADATA - START
// https://nuxt.com/docs/getting-started/seo-meta
const title = t("seo.title")
const description = t("seo.description")
useHead({
    title,
    meta: [{
        name: "description",
        content: description
    }]
})
useServerSeoMeta({
    title,
    ogTitle: title,
    description: description,
    ogDescription: description,
    ogImage: "https://globalhealthstudybuilder.org/img/social-header.png"
})
// METADATA - END
</script>