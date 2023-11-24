<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div
            v-if="appSettings.current.pageState === 'done' && pathwayStore.term && pathwayStore.term.hasOwnProperty('title')">
            <PathwayViewHeadingPanel :title="pathwayStore.term.title as string" @set-edit-request="watchHeadingRequest" />
            <JourneyStartPersonalPathBanner
                v-if="!authStore.activePathway && pathwayStore.term.pathType === 'PERSONAL' && pathwayStore.term.journeyPath"
                :journey-id="pathwayStore.term.journeyPath as string" />
            <JourneyStartResearchPathBanner v-if="authStore.completedPathway && pathwayStore.term.pathType === 'RESEARCH'"
                :pathway-id="pathwayStore.term.id as string" :pathway-title="pathwayStore.term.title as string" />
            <PathwayViewCard :pathway="pathwayStore.term" />
            <PathwayViewThemeCard v-if="pathwayStore.term.themes && pathwayStore.term.themes.length" :themes="pathwayStore.term.themes" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useAuthStore, useSettingStore, usePathwayStore } from "@/stores"

const { t } = useI18n()
const localePath = useLocalePath()
const appSettings = useSettingStore()
const route = useRoute()
const pathwayStore = usePathwayStore()
const authStore = useAuthStore()

async function watchHeadingRequest(request: string) {
    switch (request) {
        case "feature":
            await pathwayStore.toggleFeatured(route.params.id as string)
            break
        case "remove":
            await pathwayStore.removeTerm(route.params.id as string)
            return await navigateTo(localePath("/pathway"))
        case "edit":
            return await navigateTo(localePath(`/pathway/edit/${route.params.id}`))
    }
}

onMounted(async () => {
    appSettings.setPageName("nav.pathways")
    appSettings.setPageState("loading")
    await pathwayStore.getTerm(route.params.id as string)
    if (!pathwayStore.term || Object.keys(pathwayStore.term).length === 0)
        throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
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