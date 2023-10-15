<template>
    <nav class="flex border-b border-gray-200 pb-3" aria-label="Breadcrumb">
        <ol role="list" class="flex items-center space-x-4">
            <li>
                <div>
                    <LocaleLink to="/" class="text-gray-400 hover:text-gray-500">
                        <PhHouseSimple class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                        <span class="sr-only">{{ t("nav.home") }}</span>
                    </LocaleLink>
                </div>
            </li>
            <li v-if="props.project.id" class="flex items-center">
                <svg class="h-5 w-5 flex-shrink-0 text-gray-300" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                </svg>
                <LocaleLink :to="`/pathway/${props.project.id}`"
                    class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700">{{ props.project.title }}
                </LocaleLink>
            </li>
        </ol>
    </nav>
</template>

<script setup lang="ts">
import { PhHouseSimple } from "@phosphor-icons/vue"
import { ISummary } from "@/interfaces"

const { t } = useI18n()
const props = defineProps<{
    project: ISummary,
}>()
</script>