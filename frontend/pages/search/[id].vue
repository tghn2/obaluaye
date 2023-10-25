<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done' && searchStore.term && searchStore.term.hasOwnProperty('name')">
            <SearchHeadingView :title="searchStore.term.title as string" />
            <TabGroup>
                <TabList class="flex space-x-8 border-b border-gray-200 text-xs">
                    <Tab v-for="tab in navigation" :key="`tab-${tab.id}`" as="template" v-slot="{ selected }">
                        <button
                            :class="[selected ? 'border-kashmir-500 text-kashmir-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'group inline-flex items-center border-b-2 py-4 px-1 font-medium']">
                            <component :is="tab.icon"
                                :class="[selected ? 'text-kashmir-500' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']"
                                aria-hidden="true" />
                            <span>{{ t(tab.name) }}</span>
                        </button>
                    </Tab>
                </TabList>
                <TabPanels>
                    <TabPanel>
                        <SearchPathwayResponseCard :group-id="(route.params.id as string)" />
                    </TabPanel>
                    <TabPanel>
                        <GroupMetadataCard :summary="searchStore.term" />
                    </TabPanel>
                </TabPanels>
            </TabGroup>
        </div>
    </div>
</template>

<script setup lang="ts">
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue"
import { PhGraph, PhPath } from "@phosphor-icons/vue"
import { useSettingStore, useSearchStore } from "@/stores"

const { t } = useI18n()
const appSettings = useSettingStore()
const route = useRoute()
const searchStore = useSearchStore()
let navigation = [
    { name: "group.nav.response", id: "RESPONSE", icon: PhPath },
    { name: "group.nav.metadata", id: "METADATA", icon: PhGraph },
]

onMounted(async () => {
    appSettings.setPageName("nav.search")
    appSettings.setPageState("loading")
    await searchStore.getTerm(route.params.id as string)
    if (!searchStore.term || Object.keys(searchStore.term).length === 0)
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
    ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>