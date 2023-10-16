<template>
    <div v-if="journeyStore.term && journeyStore.term.hasOwnProperty('pathway')"
        class="sticky top-0 z-20 h-16 shrink-0 bg-white/75">
        <div class="sticky top-0 z-20 flex shrink-0 items-center gap-x-4 bg-white/75 sm:gap-x-6">
            <div class="flex w-full items-center justify-between gap-x-6 pb-2">
                <div class="flex items-center justify-left w-full space-x-4 truncate">
                    <div class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-kashmir-500">
                        <PhPath class="h-5 w-5 text-white" aria-hidden="true" />
                    </div>
                    <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
                        {{ journeyStore.term!.title }}
                    </h1>
                </div>
            </div>
        </div>
        <nav class="flex border-b border-gray-200 pb-3" aria-label="Breadcrumb">
            <ol role="list" class="flex items-center space-x-2">
                <li>
                    <LocaleLink to="/" class="text-gray-400 hover:text-gray-500">
                        <PhHouseSimple class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                        <span class="sr-only">{{ t("nav.home") }}</span>
                    </LocaleLink>
                </li>
                <li class="flex items-center">
                    <svg class="h-5 w-5 flex-shrink-0 text-gray-300" fill="currentColor" viewBox="0 0 20 20"
                        aria-hidden="true">
                        <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                    </svg>
                    <LocaleLink :to="`/pathway/${journeyStore.term!.pathway!.id}`"
                        class="ml-2 text-sm font-medium text-gray-500 hover:text-gray-700">{{
                            journeyStore.term!.pathway!.title }}
                    </LocaleLink>
                </li>
                <li class="flex items-center">
                    <svg class="h-5 w-5 flex-shrink-0 text-gray-300" fill="currentColor" viewBox="0 0 20 20"
                        aria-hidden="true">
                        <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                    </svg>
                </li>
                <li v-for="o in Array(journeyStore.term!.pathway!.order as number + 1).fill(0).map((_, i) => i + 1)"
                    :key="`step-${o}`" class="flex items-center">
                    <svg :class="[journeyStore.term!.order === o - 1 ? 'text-kashmir-500' : 'text-gray-300', 'h-5 w-5 flex-shrink-0']"
                        fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <circle cx="10" cy="10" r="6" />
                    </svg>
                </li>
            </ol>
        </nav>
    </div>
</template>


<script setup lang="ts">
import { PhPath, PhHouseSimple } from "@phosphor-icons/vue"
import { useJourneyStore } from "@/stores"

const { t } = useI18n()
const journeyStore = useJourneyStore()
</script>