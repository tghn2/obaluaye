<template>
    <div class="sticky top-0 z-20 h-16 shrink-0 bg-white/75">
        <div class="sticky top-0 z-20 flex shrink-0 items-center gap-x-4 bg-white/75 sm:gap-x-6">
            <div class="flex w-full items-center justify-between gap-x-6 pb-2">
                <div class="flex items-center justify-left w-full space-x-4 truncate">
                    <div class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-kashmir-500">
                        <PhPath class="h-5 w-5 text-white" aria-hidden="true" />
                    </div>
                    <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
                        {{ props.title }}
                    </h1>
                </div>
                <div class="flex flex-inline items-center space-x-2">
                    <!-- Separator -->
                    <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />
                    <button type="button" @click.prevent="watchSaveRequest('save')"
                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                        :disabled="journeyStore.savingDraft">
                        <svg v-if="journeyStore.savingDraft" aria-hidden="true"
                            class="md:-ml-0.5 h-4 w-4 text-kashmir-200 animate-spin fill-white" viewBox="0 0 100 101"
                            fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                fill="currentColor" />
                            <path
                                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                fill="currentFill" />
                        </svg>
                        <PhUpload v-else class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                        <span v-if="journeyStore.savingDraft" class="hidden md:block">{{ t("header.saving") }}</span>
                        <span v-else class="hidden md:block">{{ t("header.save") }}</span>
                    </button>
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
                    <LocaleLink
                        v-if="journeyStore.term && journeyStore.term.hasOwnProperty('pathway')"
                        :to="`/pathway/${journeyStore.term!.pathway!.id}`"
                        class="ml-2 text-sm font-medium text-gray-500 hover:text-gray-700">
                            {{ journeyStore.term!.pathway!.title }}
                    </LocaleLink>
                    <LocaleLink
                        v-else
                        to="/settings"
                        class="ml-2 text-sm font-medium text-gray-500 hover:text-gray-700">
                            {{ props.title }}
                    </LocaleLink>
                </li>
                <li 
                    v-if="journeyStore.term && journeyStore.term.hasOwnProperty('pathway')"
                    class="flex items-center">
                    <svg class="h-5 w-5 flex-shrink-0 text-gray-300" fill="currentColor" viewBox="0 0 20 20"
                        aria-hidden="true">
                        <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                    </svg>
                </li>
                <li 
                    v-if="journeyStore.term && journeyStore.term.hasOwnProperty('pathway')"
                    class="flex items-center">
                    <svg :class="[journeyStore.term!.pathway_id === route.params.id as string ? 'text-kashmir-500' : 'text-gray-300', 'h-5 w-5 flex-shrink-0']"
                        fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <circle cx="10" cy="10" r="6" />
                    </svg>
                </li>
                <li 
                    v-if="journeyStore.term && journeyStore.term.hasOwnProperty('pathway')"
                    v-for="o in Array(journeyStore.term!.pathway!.order as number + 1).fill(0).map((_, i) => i + 1)"
                    :key="`step-${o}`" class="flex items-center">
                    <svg :class="[
                            (journeyStore.term!.order === o - 1)
                            && (journeyStore.term!.pathway_id !== route.params.id as string)
                            ? 'text-kashmir-500'
                            : 'text-gray-300', 'h-5 w-5 flex-shrink-0']"
                        fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <circle cx="10" cy="10" r="6" />
                    </svg>
                </li>
            </ol>
        </nav>
    </div>
</template>


<script setup lang="ts">
import { PhPath, PhHouseSimple, PhUpload } from "@phosphor-icons/vue"
import { useJourneyStore } from "@/stores"

const { t } = useI18n()
const route = useRoute()
const journeyStore = useJourneyStore()
const props = defineProps<{
    title: string,
}>()
const emit = defineEmits<{ setSaveRequest: [request: string] }>()

async function watchSaveRequest(request: string) {
    emit("setSaveRequest", request)
}
</script>