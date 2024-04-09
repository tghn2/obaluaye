<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="readyState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-else>
            <TabGroup>
                <TabList class="flex space-x-4 border-b border-gray-200 text-xs">
                    <Tab v-for="tab in navigation" :key="`tab-${tab.id}`" as="template" v-slot="{ selected }">
                        <button
                            :class="[selected ? 'border-kashmir-500 text-kashmir-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'group inline-flex items-center border-b-2 py-4 px-1 font-medium']">
                            <component :is="tab.icon"
                                :class="[selected ? 'text-kashmir-500' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']"
                                aria-hidden="true" />
                            <span class="hidden xl:block">{{ t(tab.name) }}</span>
                        </button>
                    </Tab>
                </TabList>
                <TabPanels>
                    <TabPanel>
                        <ModerationCollectionTable />
                    </TabPanel>
                    <TabPanel>
                        <ModerationUserTable />
                    </TabPanel>
                </TabPanels>
            </TabGroup>
        </div>
    </div>
</template>

<script setup lang="ts">
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue"
import { PhUsersThree, PhRows } from "@phosphor-icons/vue"
import { useAuthStore, useSettingStore } from "@/stores"

definePageMeta({
    middleware: ["authenticated"],
});

const { t } = useI18n()
const appSettings = useSettingStore()
const authStore = useAuthStore()

let navigation = [
    { name: "settings.nav.collection", id: "COLLECTION", icon: PhRows },
    { name: "settings.nav.moderation", id: "MODERATION", icon: PhUsersThree },
]
const readyState = ref("loading")

onMounted(() => {
    appSettings.setPageName("nav.moderation")
    appSettings.setPageState("loading")
    readyState.value = "done"
})
</script>