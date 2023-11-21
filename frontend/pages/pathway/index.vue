<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6">
        <ClientOnly>
            <PathwayImportCard v-if="authStore.isAdmin" @set-import="watchImport" />
        </ClientOnly>
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done'">
            <PathwayFilterPanel />
            <div v-if="pathwayStore.multi.length === 0" class="space-y-2">
                <CommonEmptyCard :term="`${t('pathway.empty')}`" />
            </div>
            <ul role="list" class="divide-y divide-gray-100">
                <li v-for="pathway in pathwayStore.multi" :key="`pathway-${pathway.id}`"
                    class="flex items-center justify-between gap-x-6 py-5">
                    <PathwayCard :pathway="pathway" />
                </li>
            </ul>
            <CommonPagination />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSettingStore, usePathwayStore, useAuthStore } from "@/stores"
import { IPathway } from "@/interfaces"

const { t } = useI18n()
const localePath = useLocalePath()
const route = useRoute()
const appSettings = useSettingStore()
const authStore = useAuthStore()
const pathwayStore = usePathwayStore()

watch(() => [route.query], async () => {
    await updateMulti()
})

async function updateMulti() {
    if (route.query && route.query.page) pathwayStore.setPage(route.query.page as string)
    await pathwayStore.getMulti()
}

async function watchImport(payload: IPathway) {
    await pathwayStore.createImportTerm(payload)
    if (!pathwayStore.savingDraft && pathwayStore.term && pathwayStore.term.hasOwnProperty('id'))
        return await navigateTo(localePath(`/pathway/${pathwayStore.term.id}`))
}

onMounted(async () => {
    appSettings.setPageName("nav.pathways")
    updateMulti()
})

onBeforeUnmount(() => {
    const router = useRouter()
    router.replace({ query: {} })
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
    ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>