<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6">
        <ClientOnly>
            <div v-if="authStore.isAdmin"
                class="mt-6 flex justify-center space-x-10 border-b border-t border-gray-200 py-6 md:px-12">
                <LocaleLink :to="`/pathway/edit/${generateUUID()}`"
                    class="flex items-center space-x-2 rounded-lg hover:bg-gray-50 pr-1">
                    <div class="bg-kashmir-500 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg">
                        <PhPath class="h-6 w-6 text-white" aria-hidden="true" />
                    </div>
                    <h3 class="text-sm font-bold text-gray-900">
                        {{ t("pathway.create") }}
                    </h3>
                </LocaleLink>
            </div>
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
import { PhPath } from "@phosphor-icons/vue"
import { useSettingStore, usePathwayStore, useAuthStore } from "@/stores"
import { generateUUID } from "@/utilities"

const { t } = useI18n()
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