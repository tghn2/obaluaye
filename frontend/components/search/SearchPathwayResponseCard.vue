<template>
    <div class="w-full">
        <div>
            <div v-if="journeyStore.term.pathway" class="py-1 mt-4 sm:px-6">
                <CommonSummaryCard :summary="journeyStore.term.pathway" :pathway="true" />
                <div class="bg-gray-100 p-1">
                    <div class="group inline-flex text-xs font-medium text-gray-700">
                        <PhSwatches class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                        <span class="ml-1">
                            {{ journeyStore.term.title }}
                        </span>
                    </div>
                </div>
                <JourneyResponseThemeCard :theme="journeyStore.term" />
                <div v-for="node in journeyStore.term.nodes" :key="`node-${node.id}`">
                    <SearchReviewNodeCard :node="node" />
                </div>
            </div>
            <JourneyResponsePagination :last-page="lastPage" :next-page="nextPage" :editing="false"
                @set-page-response="watchPageRequest" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhSwatches } from "@phosphor-icons/vue"
import { useJourneyStore, useGroupStore } from "@/stores"

const journeyStore = useJourneyStore()
const groupStore = useGroupStore()
const nextPage = ref(false)
const lastPage = ref(false)

async function watchPageRequest(request: string) {
    switch (request) {
        case "last":
            if (lastPage.value && journeyStore.term.journeyBack) await getPathwayPage(journeyStore.term.journeyBack)
            break
        case "next":
            if (
                nextPage.value
                && journeyStore.term.journeyPath
                && journeyStore.term.journeyPath.length === 1
            ) await getPathwayPage(journeyStore.term.journeyPath[0])
            break
        default:
            break
    }
}

async function getPathwayPage(key: string) {
    // use any uuid because we don't need it to get the first theme
    await journeyStore.getGroupTerm(key, groupStore.term.id as string, false)
    if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length) nextPage.value = true
    else nextPage.value = false
    if (journeyStore.term.journeyBack) lastPage.value = true
    else lastPage.value = false
}

onMounted(async () => {
    await getPathwayPage(groupStore.term.id as string)
})
</script>