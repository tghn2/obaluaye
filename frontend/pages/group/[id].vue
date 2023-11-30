<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done' && groupStore.term && groupStore.term.hasOwnProperty('name')">
            <GroupHeadingView purpose="Group" :title="groupStore.term.title as string"
                @set-edit-request="watchHeadingRequest" />
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
                        <GroupPathwayResponseCard :group-id="(route.params.id as string)" />
                    </TabPanel>
                    <TabPanel>
                        <GroupMetadataCard :summary="groupStore.term" />
                    </TabPanel>
                    <TabPanel>
                        <GroupMembersCard :group-id="(route.params.id as string)" />
                    </TabPanel>
                    <TabPanel>
                        <GroupInvitationsCard :group-id="(route.params.id as string)" />
                    </TabPanel>
                </TabPanels>
            </TabGroup>
        </div>
    </div>
</template>

<script setup lang="ts">
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue"
import { PhEnvelopeSimple, PhUsersThree, PhGraph, PhPath } from "@phosphor-icons/vue"
import { useSettingStore, useGroupStore, useAuthStore } from "@/stores"

definePageMeta({
    middleware: ["authenticated"],
})

const { t } = useI18n()
const localePath = useLocalePath()
const appSettings = useSettingStore()
const route = useRoute()
const groupStore = useGroupStore()
const authStore = useAuthStore()
let navigation = [
    { name: "group.nav.response", id: "RESPONSE", icon: PhPath },
    { name: "group.nav.metadata", id: "METADATA", icon: PhGraph },
    { name: "group.nav.members", id: "MEMBERS", icon: PhUsersThree },
    { name: "group.nav.invitations", id: "INVITATIONS", icon: PhEnvelopeSimple }
]

async function watchHeadingRequest(request: string) {
    switch (request) {
        case "feature":
            await groupStore.toggleFeatured(route.params.id as string)
            // await groupStore.getTerm(route.params.id as string, false)
            break
        case "complete":
            await groupStore.toggleCompleted(route.params.id as string)
            break
        case "remove":
            if (groupStore.isLastMember || authStore.isAdmin) {
                await groupStore.removeTerm(route.params.id as string)
                return await navigateTo(localePath("/group"))
            }
        case "edit":
            if (groupStore.isResearcher || groupStore.isCustodian || authStore.isAdmin) {
                return await navigateTo(localePath(`/group/edit/${route.params.id}`))
            }
    }
}

onMounted(async () => {
    appSettings.setPageName("nav.groups")
    appSettings.setPageState("loading")
    await groupStore.getTerm(route.params.id as string)
    if (!groupStore.term || Object.keys(groupStore.term).length === 0)
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