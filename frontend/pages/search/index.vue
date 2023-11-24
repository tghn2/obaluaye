<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6">
        <SearchFilterPanel />
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done'">
            <div v-if="searchStore.multi.length === 0" class="space-y-2">
                <CommonEmptyCard :term="`${t('search.empty')}`" />
            </div>
            <ul v-else role="list" class="divide-y divide-gray-100">
                <li v-for="group in searchStore.multi" :key="`search-${group.id}`"
                    class="flex items-center justify-between gap-x-6 py-5">
                    <SearchCard :group="group" />
                </li>
            </ul>
            <CommonPagination />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSettingStore, useSearchStore } from "@/stores"

const { t } = useI18n()
const route = useRoute()
const appSettings = useSettingStore()
const searchStore = useSearchStore()

watch(() => [route.query], async () => {
    await updateMulti()
})

async function updateMulti() {
    if (route.query && route.query.page) searchStore.setPage(route.query.page as string)
    await searchStore.getMulti()
}

onMounted(async () => {
    appSettings.setPageName("nav.search")
    await updateMulti()
    // searchStore.settings.setPageState("done")
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
    ogImage: "https://globalhealthstudybuilder.org/img/social-header.png"
})
// METADATA - END
</script>