<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done'">
            <GroupFilterPanel />
            <GuidepathStartPersonalJourney v-if="authStore.loggedIn && !authStore.completedPathway" />
            <GuidepathStartStudyJourney v-if="authStore.loggedIn && authStore.completedPathway" />
            <div v-if="groupStore.multi.length === 0" class="space-y-2">
                <CommonEmptyCard v-if="authStore.completedPersonalPathway" :term="`${t('group.empty')}`" />
                <CommonEmptyCard v-else :term="`${t('group.emptyIncomplete')}`" />
            </div>
            <ul role="list" class="divide-y divide-gray-100">
                <li v-for="group in groupStore.multi" :key="`group-${group.id}`"
                    class="flex items-center justify-between gap-x-6 py-5">
                    <GroupCard :group="group" />
                </li>
            </ul>
            <CommonPagination />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSettingStore, useGroupStore, useAuthStore } from "@/stores"

definePageMeta({
    middleware: ["authenticated"],
})

const { t } = useI18n()
const route = useRoute()
const appSettings = useSettingStore()
const authStore = useAuthStore()
const groupStore = useGroupStore()

watch(() => [route.query], async () => {
    await updateMulti()
})

async function updateMulti() {
    if (route.query && route.query.page) groupStore.setPage(route.query.page as string)
    await groupStore.getMulti()
}

onMounted(async () => {
    appSettings.setPageName("nav.groups")
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
    ogImage: "https://globalhealthstudybuilder.org/img/social-header.png"
})
// METADATA - END
</script>