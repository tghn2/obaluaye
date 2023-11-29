<template>
    <div class="flex space-x-2 justify-center sm:px-6 sm:py-2 lg:px-8">
        <div v-if="route.path !== '/group'"
            class="flex items-center justify-between gap-x-6 ring-1 ring-spring-500 px-6 py-2.5 sm:rounded-xl sm:py-3 sm:pl-4 sm:pr-3.5">
            <p class="text-sm leading-6 text-gray-900">
                {{ t("pathway.journey.manageResearch") }}
            </p>
            <button @click.prevent="submit('manage')"
                class="group flex items-center gap-x-1 text-sm leading-6 font-semibold text-white rounded-md p-1 pr-2 bg-spring-600 hover:bg-spring-800">
                <PhUsersThree class="h-4 w-4" aria-hidden="true" />
                <span>{{ t("pathway.journey.continue") }}</span>
            </button>
        </div>
        <div
            class="flex items-center justify-between gap-x-6 ring-1 ring-kashmir-500 px-6 py-2.5 sm:rounded-xl sm:py-3 sm:pl-4 sm:pr-3.5">
            <p class="text-sm leading-6 text-gray-900">
                {{ t("pathway.journey.startResearch") }}
            </p>
            <button @click.prevent="submit('start')"
                class="group flex items-center gap-x-1 text-sm leading-6 font-semibold text-white rounded-md p-1 pr-2 bg-kashmir-600 hover:bg-kashmir-800">
                <PhPlay class="h-4 w-4" aria-hidden="true" />
                <span>{{ t("pathway.journey.start") }}</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhUsersThree, PhPlay } from "@phosphor-icons/vue"
import { usePathwayStore } from "@/stores"

const { t } = useI18n()
const route = useRoute()
const localePath = useLocalePath()
const pathwayStore = usePathwayStore()

async function submit(request: string) {
    switch (request) {
        case "manage":
            return await navigateTo(localePath("/group"))
        case "start":
            await pathwayStore.getFeaturedTerm()
            if (pathwayStore.termStudy) {
                return await navigateTo(localePath(`/pathway/${pathwayStore.termStudy}`))
            }
            break
    }
}
</script>