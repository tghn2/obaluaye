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
                            <span v-if="tab.showDot" class="relative">
                                <svg viewBox="0 0 100 100" class="absolute -ml-1 sm:-ml-0 -mt-2 z-10 h-[2rem] w-[2rem]"
                                    aria-hidden="true">
                                    <circle cx="10" cy="10" r="10" fill="#d93e8a" />
                                </svg>
                            </span>
                        </button>
                    </Tab>
                </TabList>
                <TabPanels>
                    <TabPanel v-if="authStore.activePathway">
                        <SettingsPathwayCard />
                    </TabPanel>
                    <TabPanel>
                        <SettingsProfile />
                    </TabPanel>
                    <TabPanel>
                        <SettingsInvitationsCard />
                    </TabPanel>
                    <TabPanel>
                        <SettingsSecurity />
                    </TabPanel>
                    <TabPanel v-if="authStore.isAdmin">
                        <ModerationUserTable />
                    </TabPanel>
                </TabPanels>
            </TabGroup>
        </div>
    </div>
</template>

<script setup lang="ts">
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue"
import { PhKey, PhUserCircle, PhEnvelopeSimple, PhUsersThree, PhPath } from "@phosphor-icons/vue"
import { useAuthStore, useSettingStore } from "@/stores"

definePageMeta({
    middleware: ["authenticated"],
});

const { t } = useI18n()
const appSettings = useSettingStore()
const authStore = useAuthStore()

let navigation = [
    { name: "settings.nav.account", id: "ACCOUNT", icon: PhUserCircle, showDot: false },
    { name: "settings.nav.invitations", id: "INVITATIONS", icon: PhEnvelopeSimple, showDot: authStore.profile.invitationCount > 0 },
    { name: "settings.nav.security", id: "SECURITY", icon: PhKey, showDot: false },
]
const readyState = ref("loading")

onMounted(() => {
    appSettings.setPageName("nav.settings")
    appSettings.setPageState("loading")
    if (authStore.activePathway) navigation.unshift(
        { name: "settings.nav.pathway", id: "PATHWAY", icon: PhPath, showDot: false },
    )
    if (authStore.isAdmin) navigation.push(
        { name: "settings.nav.moderation", id: "MODERATION", icon: PhUsersThree, showDot: false },
    )
    readyState.value = "done"
})
</script>