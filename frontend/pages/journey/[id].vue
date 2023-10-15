<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div
            v-if="appSettings.current.pageState === 'done' && journeyStore.term && journeyStore.term.hasOwnProperty('name')">
            <JourneyResponseHeadingPanel :title="journeyStore.term.pathway!.title as string"
                @set-edit-request="watchHeadingRequest" />
            <JourneyResponseThemeCard :theme="journeyStore.term" />
            <div v-for="node in journeyStore.term.nodes" :key="`node-${node.id}`" class="sm:px-6">
                <JourneyResponseNodeCard :node="node" @set-response="watchResponseUpdate" />
            </div>
            <div class="flex justify-end sm:px-8 mt-3">
                <button type="button" @click.prevent="watchHeadingRequest('save')"
                    class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md border border-transparent bg-spring-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-spring-700 focus:outline-none focus:ring-2 focus:ring-spring-600 focus:ring-offset-2"
                    :disabled="journeyStore.savingDraft">
                    <svg v-if="journeyStore.savingDraft" aria-hidden="true"
                        class="md:-ml-0.5 h-4 w-4 text-white animate-spin fill-white" viewBox="0 0 100 101" fill="none"
                        xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                            fill="currentColor" />
                        <path
                            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                            fill="currentFill" />
                    </svg>
                    <PhUploadSimple v-else class="md:-ml-0.5 h-4 w-4 text-white" aria-hidden="true" />
                    <span v-if="journeyStore.savingDraft" class="hidden md:block">{{ t("pathway.journey.saving") }}</span>
                    <span v-else class="hidden md:block">
                        <span v-if="journeyStore.term.journeyPath && journeyStore.term.journeyPath.length">
                            {{ t("pathway.journey.saveNext") }}
                        </span>
                        <span v-else>{{ t("pathway.journey.save") }}</span>
                    </span>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhUploadSimple } from "@phosphor-icons/vue"
import { useSettingStore, useJourneyStore } from "@/stores"
import { IResponse, INode, ITerm } from "@/interfaces"

const { t } = useI18n()
const localePath = useLocalePath()
const appSettings = useSettingStore()
const route = useRoute()
const journeyStore = useJourneyStore()
const draftResponse = ref([] as IResponse[])

onMounted(async () => {
    appSettings.setPageName("nav.pathways")
    appSettings.setPageState("loading")
    await journeyStore.getTerm(route.params.id as string)
    if (!journeyStore.term || Object.keys(journeyStore.term).length === 0)
        throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
})

// WATCHERS
async function watchHeadingRequest(request: string) {
    console.log("watchHeadingRequest", request)
    switch (request) {
        case "save":
            await journeyStore.createTerm(draftResponse.value)
            if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length === 1)
                return await navigateTo(localePath(`/journey/${journeyStore.term.journeyPath[0]}`))
            if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length > 1)
                await navigateToSelectedBranch()
            // Else end of path and navigate to either Group or Personal path review
            break
        case "cancel":
            return await navigateTo(localePath("/pathway/"))
        default:
            break
    }
}

function watchResponseUpdate(response: IResponse) {
    if (response.node_id) {
        const responseIdx = draftResponse.value.findIndex(rspns => rspns.node_id === response.node_id)
        // console.log("watch", appSettings.current.pageState, responseIdx, response.id, response.node_id)
        if (responseIdx >= 0) {
            draftResponse.value[responseIdx] = { ...response }
        } else {
            draftResponse.value.push({ ...response })
        }
    }
}

// UTILITIES
async function navigateToSelectedBranch() {
    const lastResponse = draftResponse.value.slice(-1)[0]
    if (lastResponse && journeyStore.term.nodes && journeyStore.term.nodes.length) {
        const branchedNode = journeyStore.term.nodes.find(
            (node: INode) => node.id === lastResponse.node_id
        )
        if (
            branchedNode
            && branchedNode.form
            && branchedNode.form.terms
            && branchedNode.form.terms.length
            && lastResponse.answer
            && !Array.isArray(lastResponse.answer)
            && lastResponse.answer.id
        ) {
            const answerID = lastResponse.answer.id
            const nextTheme = branchedNode.form.terms.find(
                (term: ITerm) => term.id === answerID
            )
            if (nextTheme && nextTheme.branch) return await navigateTo(localePath(`/journey/${nextTheme.branch}`))
        }
    }
}

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