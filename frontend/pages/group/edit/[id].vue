<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done' && groupStore.term && groupStore.term.hasOwnProperty('name')">
            <GroupHeadingEditView :title="groupStore.term.title as string" @set-edit-request="watchHeadingRequest" />
            <form class="flex-auto rounded-lg p-3">
                <div class="grid grid-cols-1 gap-x-3 gap-y-4 sm:grid-cols-6">
                    <div class="sm:col-span-5">
                        <label for="group-title" class="block text-sm font-semibold leading-6 text-gray-900">{{
                            t("group.field.title") }}</label>
                        <div class="mt-2">
                            <input type="text" name="group-title" id="group-title" v-model="draft.title"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
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
                        <div class="mt-2">
                            <textarea id="description" name="description" rows="3" v-model="draft.description"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                        </div>
                        <p class="mt-2 text-sm leading-6 text-gray-500">
                            <span>{{ t("group.help.description") }}</span>
                        </p>
                    </div>
                    <div class="col-span-full">
                        <label for="group-subject-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.subjects") }}
                        </label>
                        <div class="mt-2">
                            <input type="text" name="group-subject-values" id="group-subject-values" v-model="subjects"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                        </div>
                        <p class="mt-2 text-sm leading-6 text-gray-500">{{ t("group.help.subjects") }}</p>
                    </div>
                    <div class="col-span-full">
                        <label for="group-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.country") }}
                        </label>
                        <div class="mt-2">
                            <CommonCountrySelect :initial-choices="draft.country" @set-select="watchCountrySelect" />
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
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSettingStore, useGroupStore } from "@/stores"
import { IGroup } from "@/interfaces"

definePageMeta({
    middleware: ["authenticated"],
})

const { t } = useI18n()
const localePath = useLocalePath()
const appSettings = useSettingStore()
const route = useRoute()
const groupStore = useGroupStore()
const draft = ref({} as IGroup)
const subjects = ref("")
const groupTitle = ref("group.creating")

// WATCHERS
async function watchHeadingRequest(request: string) {
    switch (request) {
        case "save":
            saveDraft()
            await groupStore.updateTerm(route.params.id as string)
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

watch(
    () => draft.value, () => {
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
const title = "whyqd.com — more research, less wrangling"
const description = "Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods."
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
    ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>