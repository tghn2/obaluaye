<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div
            v-if="appSettings.current.pageState === 'done' && journeyStore.term && journeyStore.term.hasOwnProperty('name')">
            <JourneyResponseHeadingPanel :title="journeyStore.term.pathway!.title as string" />
            <div class="mt-4 sm:px-6">
                <JourneyResponseThemeCard :theme="journeyStore.term" />
            </div>
            <div v-for="node in journeyStore.term.nodes" :key="`node-${node.id}`" class="sm:px-6">
                <JourneyResponseNodeCard :node="node" @set-response="watchResponseUpdate" />
            </div>
            <JourneyResponsePagination :last-page="lastPage" :next-page="nextPage" :editing="true"
                @set-page-response="watchPageRequest" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSettingStore, useJourneyStore } from "@/stores"
import { IResponse, INode, ITerm } from "@/interfaces"

const { t } = useI18n()
const localePath = useLocalePath()
const appSettings = useSettingStore()
const route = useRoute()
const journeyStore = useJourneyStore()
const draftResponse = ref([] as IResponse[])
const nextPage = ref(false)
const lastPage = ref(false)

onMounted(async () => {
    appSettings.setPageName("nav.pathways")
    appSettings.setPageState("loading")
    await journeyStore.getGroupTerm(route.params.id as string, route.params.group as string)
    if (!journeyStore.term || Object.keys(journeyStore.term).length === 0)
        throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
    if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length) nextPage.value = true
    else nextPage.value = false
    if (journeyStore.term.journeyBack) lastPage.value = true
    else lastPage.value = false
})

// WATCHERS
async function watchPageRequest(request: string) {
    switch (request) {
        case "last":
            if (journeyStore.term.journeyBack)
                return await navigateTo(localePath(`/journey/${route.params.group as string}/${journeyStore.term.journeyBack}`))
            break
        case "next":
            await journeyStore.createTerm(draftResponse.value)
            if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length === 1)
                return await navigateTo(localePath(`/journey/${route.params.group as string}/${journeyStore.term.journeyPath[0]}`))
            if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length > 1)
                await navigateToSelectedBranch()
            if (
                journeyStore.term.journeyPath
                && journeyStore.term.journeyPath.length === 0
                && journeyStore.sourceGroup
            ) return await navigateTo(localePath(`/group/${journeyStore.sourceGroup}`))
            else return await navigateTo(localePath("/group"))
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
    ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>