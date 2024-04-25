<template>
    <div class="w-full">
        <div class="space-y-6 bg-white py-6 px-4 sm:p-6">
            <div class="flex justify-between">
                <div>
                    <h3 class="text-lg font-medium leading-6 text-gray-900">{{ t("settings.account.title") }}</h3>
                    <p class="mt-1 text-sm text-gray-500">
                        {{ t("settings.pathway.description") }}
                    </p>
                </div>
                <LocaleLink
                    :to="`/journey/${pathwayStore.termPersonal ? journeyStore.term.pathway_id : authStore.profile.id}`"
                    class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 my-1 text-sm ring-1 ring-inset text-white bg-spring-500 hover:bg-spring-700">
                    <PhPencilSimple class="md:-ml-0.5 h-4 w-4" aria-hidden="true" />
                    <span class="hidden md:block">{{ t("pathway.journey.review") }}</span>
                </LocaleLink>
            </div>
            <div v-if="profilePage">
                <div class="space-y-1 grid grid-cols-1 gap-x-3 gap-y-4 sm:grid-cols-6">
                    <div v-if="authStore.profile.full_name" class="sm:col-span-5">
                        <div class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.account.profileName") }}
                        </div>
                        <div class="block text-sm leading-6 text-gray-900">
                            {{ authStore.profile.full_name }}
                        </div>
                    </div>
                    <div v-if="authStore.profile.language" class="sm:col-span-1">
                        <div class="block text-sm font-semibold leading-6 text-gray-900 -mt-1">
                            {{ t("group.field.language") }}
                        </div>
                        <div class="block text-sm leading-6 text-gray-900">
                            <CommonLocaleView :language="authStore.profile.language" />
                        </div>
                    </div>
                    <div class="col-span-full">
                        <div class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.account.email") }}
                        </div>
                        <div class="block text-sm leading-6 text-gray-900">
                            {{ authStore.profile.email }}
                        </div>
                    </div>
                    <div v-if="authStore.profile.description" class="col-span-full">
                        <div class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.description") }}
                        </div>
                        <div class="block text-sm leading-6 text-gray-900">
                            {{ authStore.profile.description }}
                        </div>
                    </div>
                    <div v-if="authStore.profile.subjects && authStore.profile.subjects.length" class="col-span-full">
                        <div class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.field.subjects") }}
                        </div>
                        <div class="block text-sm leading-6 text-gray-900">
                            {{ authStore.profile.subjects.join(", ") }}
                        </div>
                    </div>
                    <div v-if="authStore.profile.country && authStore.profile.country.length" class="col-span-full">
                        <div for="group-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.country") }}
                        </div>
                        <div class="block text-sm leading-6 text-gray-900">
                            <CommonCountryView :current-country="authStore.profile.country" />
                        </div>
                    </div>
                    <div 
                        v-if="authStore.profile.collection && authStore.profile.collection.length"
                        v-for="collection in authStore.profile.collection"
                        :key="`profile-collection${collection.id}`"
                        class="col-span-full">
                        <div v-if="collection.selection && collection.selection.length">
                            <div for="group-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ collection.title }}
                            </div>
                            <div class="block text-sm leading-6 text-gray-900">
                                {{ collection.selection.map(({ term }) => term).join(", ") }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
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
            </div>
            <JourneyResponsePagination v-if="showPathway" :last-page="lastPage" :next-page="nextPage" :editing="false"
                @set-page-response="watchPageRequest" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPencilSimple, PhSwatches } from "@phosphor-icons/vue"
import { useAuthStore, useJourneyStore, usePathwayStore } from "@/stores"
import { IUserProfileUpdate } from "@/interfaces"

const { t } = useI18n()
const authStore = useAuthStore()
const journeyStore = useJourneyStore()
const pathwayStore = usePathwayStore()
const profile = ref({} as IUserProfileUpdate)
const subjects = ref("")
const nextPage = ref(false)
const lastPage = ref(false)
const showPathway = ref(false)
const profilePage = ref(true)

onMounted(async () => {
    resetProfile()
    if (authStore.activePathway) {
        showPathway.value = true
        await getPathwayPage(authStore.activePathway as string)
    }
})

async function watchPageRequest(request: string) {
    switch (request) {
        case "last":
            if (lastPage.value && journeyStore.term.journeyBack) {
                await getPathwayPage(journeyStore.term.journeyBack)
            } else {
                profilePage.value = true
                await getPathwayPage(authStore.activePathway as string)
            }
            break
        case "next":
            if (profilePage.value) {
                profilePage.value = false
                await getPathwayPage(authStore.activePathway as string)
            } else if (
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
    if (journeyStore.term.id && profilePage.value) nextPage.value = true
    else if (journeyStore.term.journeyPath && journeyStore.term.journeyPath.length) nextPage.value = true
    else nextPage.value = false
    if (!profilePage.value) lastPage.value = true
    else if (journeyStore.term.journeyBack) lastPage.value = true
    else lastPage.value = false
}

function resetProfile() {
    profile.value = {
        full_name: authStore.profile.full_name,
        email: authStore.profile.email,
        description: authStore.profile.description,
        subjects: authStore.profile.subjects,
        country: authStore.profile.country,
        spatial: authStore.profile.spatial,
        language: authStore.profile.language,
    }
    if (authStore.profile.subjects && authStore.profile.subjects.length) subjects.value = authStore.profile.subjects.join(", ")
}
</script>