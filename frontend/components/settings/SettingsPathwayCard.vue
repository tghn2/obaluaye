<template>
    <div class="w-full">
        <div>
            <div class="flex justify-between pt-6 px-4 sm:px-6">
                <div>
                    <h3 class="text-lg font-medium leading-6 text-gray-900">{{ t("settings.pathway.title") }}</h3>
                    <p class="mt-1 text-sm text-gray-500">
                        {{ t("settings.pathway.description") }}
                    </p>
                </div>
                <LocaleLink v-if="authStore.activePathway && journeyStore.term && journeyStore.term.pathway_id"
                    :to="`/journey/${journeyStore.term.pathway_id}`"
                    class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 my-1 text-sm ring-1 ring-inset text-white bg-spring-500 hover:bg-spring-700">
                    <PhPencilSimple class="md:-ml-0.5 h-4 w-4" aria-hidden="true" />
                    <span class="hidden md:block">{{ t("pathway.journey.review") }}</span>
                </LocaleLink>
            </div>
            <!-- <GuidepathStartStudyJourney v-if="authStore.completedPathway" /> -->
            <div v-if="journeyStore.term.pathway" class="py-1 mt-4 sm:px-6 border-t border-gray-200">
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
                    <JourneyReviewNodeCard :node="node" />
                </div>
            </div>
            <JourneyResponsePagination :last-page="lastPage" :next-page="nextPage" :editing="false"
                @set-page-response="watchPageRequest" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPencilSimple, PhSwatches, PhArrowSquareOut } from "@phosphor-icons/vue"
import { useAuthStore, useJourneyStore } from "@/stores"

const { t } = useI18n()
const journeyStore = useJourneyStore()
const authStore = useAuthStore()
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
    await journeyStore.getTerm(key, false)
    if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length) nextPage.value = true
    else nextPage.value = false
    if (journeyStore.term.journeyBack) lastPage.value = true
    else lastPage.value = false
}


onMounted(async () => {
    if (authStore.activePathway) await getPathwayPage(authStore.activePathway as string)
})
</script>