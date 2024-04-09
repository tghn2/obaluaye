<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done'">
            <CollectionEditHeadingPanel :title="draft.title as string" @set-edit-request="watchHeadingRequest" />
            <div class="flex justify-between -mb-2 mt-2">
                <div class="flex flex-inline items-center space-x-2">
                    <div
                        class="text-xs font-medium leading-6 text-white bg-kashmir-700 mx-3 px-3 pt-0.5 -mb-0.5 mt-0.5 rounded-t-lg">
                        {{ t("collection.metadata") }}
                    </div>
                    <div v-if="collectionStore.isTranslatingDraft"
                        class="relative -ml-px inline-flex items-center gap-x-1.5 text-xs">
                        <div class="rounded-full bg-spring-600 p-1">
                            <PhTranslate class="h-4 w-4 text-white" aria-hidden="true" />
                        </div>
                        <span class="text-spring-600 hidden md:block">{{ t("collection.translate") }}</span>
                    </div>
                </div>
            </div>
            <div class="rounded-lg my-2 border-t-2 border-kashmir-700">
                <form class="flex-auto rounded-lg p-3">
                    <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
                        <div class="sm:col-span-4">
                            <label for="node-question" class="block text-sm font-semibold leading-6 text-gray-900">{{
                                t("collection.title") }}</label>
                            <div class="mt-2">
                                <input type="text" name="node-question" id="node-question" v-model="draft.title"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p v-if="collectionStore.isTranslatingDraft" class="mt-2 text-sm leading-6 text-gray-500">
                                {{ collectionStore.edit.title }}
                            </p>
                        </div>
                        <div class="sm:col-span-2">
                            <SwitchGroup as="div" class="flex items-center p-3 mt-7 align-middle">
                                <Switch v-model="draft.isMulti"
                                    class="group relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer items-center justify-center rounded-full focus:outline-none">
                                    <span aria-hidden="true"
                                        class="pointer-events-none absolute h-full w-full rounded-md bg-white" />
                                    <span aria-hidden="true"
                                        :class="[draft.isMulti ? 'bg-kashmir-600' : 'bg-gray-200', 'pointer-events-none absolute mx-auto h-4 w-9 rounded-full transition-colors duration-200 ease-in-out']" />
                                    <span aria-hidden="true"
                                        :class="[draft.isMulti ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none absolute left-0 inline-block h-5 w-5 transform rounded-full border border-gray-200 bg-white shadow ring-0 transition-transform duration-200 ease-in-out']" />
                                </Switch>
                                <SwitchLabel as="span" class="ml-3 text-sm">
                                    <span class="font-medium text-gray-900">{{ t("collection.multi") }}</span>
                                </SwitchLabel>
                            </SwitchGroup>
                        </div>
                    </div>
                    <div class="border-t border-gray-500 mt-2">
                        <div class="mt-2">
                            <table class="min-w-full divide-y divide-gray-200">
                                <tbody class="divide-y divide-gray-200">
                                    <tr v-for="(term, termIdx) in draft.selection" :key="`term-${term.id}`">
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-700">
                                            <input type="text" v-model="draft.selection![termIdx].term"
                                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                                        </td>
                                        <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                                            <button type="button" @click="removeTerm(termIdx)"
                                                class="relative items-center rounded-full p-1 text-cerise-700 hover:bg-cerise-50">
                                                <PhX class="h-5 w-5" aria-hidden="true" />
                                            </button>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-700">
                                            {{ t("collection.add") }}
                                        </td>
                                        <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                                            <button type="button" @click="addTerm"
                                                class="relative items-center rounded-full p-1 text-kashmir-500 hover:bg-kashmir-100">
                                                <PhPlus class="h-5 w-5" aria-hidden="true" />
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPlus, PhX, PhTranslate } from "@phosphor-icons/vue"
import { Switch, SwitchGroup, SwitchLabel } from "@headlessui/vue"
import { useCollectionStore, useSettingStore } from "@/stores"
import { ICollection, ISelection } from "@/interfaces"
// import { generateUUID } from "@/utilities"

definePageMeta({
    middleware: ["moderator"],
});

const { t } = useI18n()
const localePath = useLocalePath()
const route = useRoute()
const appSettings = useSettingStore()
const collectionStore = useCollectionStore()
const draft = ref({} as ICollection)
const draftStartLanguage = ref("")
const { locale } = useI18n()

// SETUP
onMounted(async () => {
    appSettings.setPageName("nav.collection")
    appSettings.setPageState("loading")
    await collectionStore.getTerm(route.params.id as string, false)
    if (!collectionStore.term || Object.keys(collectionStore.term).length === 0)
        throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
    resetDraft()
    draftStartLanguage.value = draft.value.language as string
    // collectionStore.setSavingEdit(false)
    collectionStore.settings.setPageState("done")
})

function resetDraft() {
    collectionStore.setLanguageDraft(collectionStore.term.language as string)
    let temporaryDraft: ICollection = { ...collectionStore.term }
    draft.value = { ...temporaryDraft }
}

// WATCHERS
async function watchHeadingRequest(request: string) {
    // console.log("watchHeadingRequest", request)
    switch (request) {
        case "save":
            await collectionStore.createTerm(route.params.id as string, draft.value)
            break
        case "cancel":
            return await navigateTo(localePath("/moderation"))
        default:
            watchLocaleSelect(request)
            break
    }
}

function watchLocaleSelect(select: string) {
    // console.log("Language change", select)
    collectionStore.setLanguageDraft(select)
    // collectionStore.setIsTranslatingDraft(select !== draftStartLanguage.value)
}

watch(
    () => draft.value, () => {
        if (Object.keys(draft.value).length !== 0) collectionStore.setDraft({ ...draft.value })
    },
    { deep: true }
)

// SELECTION
function addTerm(): void {
    if (!draft.value.selection) draft.value.selection = []
    const newTerm: ISelection = {
        term: "",
        collection_id: draft.value.id as string,
    }
    draft.value.selection.splice(draft.value.selection.length, 1, newTerm)
}

function removeTerm(term: number): void {
    if (draft.value.selection && draft.value.selection.length) {
        if (draft.value.selection[term] && draft.value.selection[term].id)
            collectionStore.removeTermSelection(draft.value.selection[term].id as string, route.params.id as string)
        draft.value.selection.splice(term, 1)
    }
}

onBeforeRouteLeave((to, from, next) => {
    if (Object.keys(draft.value).length !== 0) collectionStore.setDraft({ ...draft.value })
    next()
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