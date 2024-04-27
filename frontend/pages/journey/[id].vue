<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div
            v-if="appSettings.current.pageState === 'done'">
            <JourneyResponseHeadingPanel :title="pageHeading" @set-save-request="watchPageRequest" />
            <JourneyResponseProfileCard v-if="profilePage" 
                :next-page="route.params.id as string !== authStore.profile.id ? journeyStore.term.id as string : authStore.profile.id" 
                @set-response="watchResponseProfileUpdate" />
            <div v-else>
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
    </div>
</template>

<script setup lang="ts">
import { useSettingStore, useAuthStore, useJourneyStore, usePathwayStore, useCollectionStore } from "@/stores"
import { IResponse, IUserProfileUpdate, INode, ITerm, ITheme } from "@/interfaces"

const { t } = useI18n()
const localePath = useLocalePath()
const appSettings = useSettingStore()
const route = useRoute()
const authStore = useAuthStore()
const pathwayStore = usePathwayStore()
const journeyStore = useJourneyStore()
const collectionStore = useCollectionStore()
const draftResponse = ref([] as IResponse[])
const nextPage = ref(false)
const lastPage = ref(false)
const profilePage = ref(false)
const pageHeading = ref(t('settings.account.title'))

onMounted(async () => {
    appSettings.setPageName("nav.pathways")
    appSettings.setPageState("loading")
    if (route.params.id as string !== authStore.profile.id) {
        await journeyStore.getTerm(route.params.id as string)
        if (!journeyStore.term || Object.keys(journeyStore.term).length === 0)
            throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
    } else {
        if (authStore.personalPathway) await journeyStore.getTerm(authStore.personalPathway as string)
        else journeyStore.setTerm({} as ITheme)
    }
    if (
        (
            route.params.id as string === authStore.profile.id
        )
        || (
            pathwayStore.termPersonal
            && (pathwayStore.termPersonal === route.params.id as string)
        )
        || (
            journeyStore.term.pathway_id === route.params.id as string
        )
     ) {
        profilePage.value = true
        collectionStore.getMulti({selections: true})
    }
    if (
        (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length)
        || profilePage.value
    ) nextPage.value = true
    else nextPage.value = false
    if (journeyStore.term.journeyBack || !profilePage.value) lastPage.value = true
    else lastPage.value = false
    if (!profilePage.value) pageHeading.value = journeyStore.term.pathway!.title as string
})

// WATCHERS
async function watchPageRequest(request: string) {
    switch (request) {
        case "save":
            await journeyStore.createTerm(draftResponse.value)
            break
        case "last":
            if (journeyStore.term.journeyBack)
                return await navigateTo(localePath(`/journey/${journeyStore.term.journeyBack}`))
            if (!profilePage.value)
                return await navigateTo(localePath(`/journey/${journeyStore.term.pathway_id}`))
            break
        case "next":
            await journeyStore.createTerm(draftResponse.value)
            if (profilePage.value)
                return await navigateTo(localePath(`/journey/${journeyStore.term.id}`))
            if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length === 1)
                return await navigateTo(localePath(`/journey/${journeyStore.term.journeyPath[0]}`))
            if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length > 1)
                await navigateToSelectedBranch()
            return await navigateTo(localePath("/settings"))
        default:
            break
    }
}

function watchResponseUpdate(response: IResponse) {
    if (response.node_id) {
        const responseIdx = draftResponse.value.findIndex(rspns => rspns.node_id === response.node_id)
        if (responseIdx >= 0) {
            draftResponse.value[responseIdx] = { ...response }
        } else {
            draftResponse.value.push({ ...response })
        }
    }
}

function watchResponseProfileUpdate(response: IUserProfileUpdate) {
    console.log("----------- profile --------------")
    console.log(response)
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
    ogImage: "https://globalhealthstudybuilder.org/img/social-header.png"
})
// METADATA - END
</script>