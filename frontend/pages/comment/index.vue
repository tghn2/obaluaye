<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done'">
            <CommentFilterPanel />
            <div v-if="commentStore.multi.length === 0" class="space-y-2">
                <CommonEmptyCard :term="`${t('comment.empty')}`" />
            </div>
            <ul role="list" class="divide-y divide-gray-100">
                <li v-for="comment in commentStore.multi" :key="`comment-${comment.id}`"
                    class="flex items-center justify-between gap-x-6 py-5">
                    <CommentCard :comment="comment" />
                </li>
            </ul>
            <CommonPagination />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useSettingStore, useCommentStore } from "@/stores"

definePageMeta({
    middleware: ["authenticated"],
})

const { t } = useI18n()
const route = useRoute()
const appSettings = useSettingStore()
const commentStore = useCommentStore()

// WATCHERS
watch(() => [route.query], async () => {
    await updateMulti()
})

// SETTERS
async function updateMulti() {
    if (route.query && route.query.page) commentStore.setPage(route.query.page as string)
    await commentStore.getMulti()
}

onMounted(async () => {
    appSettings.setPageName("nav.comments")
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