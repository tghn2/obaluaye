<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6">
        <ClientOnly>
            <div v-if="authStore.isAdmin"
                class="mt-6 flex justify-center space-x-10 border-b border-t border-gray-200 py-6 md:px-12">
                <LocaleLink :to="`/group/edit/${generateUUID()}`"
                    class="flex items-center space-x-2 rounded-lg hover:bg-gray-50 pr-1">
                    <div class="bg-spring-500 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg">
                        <PhPath class="h-6 w-6 text-white" aria-hidden="true" />
                    </div>
                    <h3 class="text-sm font-bold text-gray-900">
                        {{ t("group.create") }}
                    </h3>
                </LocaleLink>
            </div>
        </ClientOnly>
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done'">
            <GroupFilterPanel />
            <div v-if="groupStore.multi.length === 0" class="space-y-2">
                <CommonEmptyCard :term="`${t('group.empty')}`" />
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
import { PhPath } from "@phosphor-icons/vue"
import { useSettingStore, useGroupStore, useAuthStore } from "@/stores"
import { generateUUID } from "@/utilities"

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