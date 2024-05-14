<template>
    <nav class="flex" aria-label="Breadcrumb">
        <ol role="list" class="flex items-center space-x-2">
            <li>
                <LocaleLink to="/" class="text-gray-400 hover:text-gray-500">
                    <PhHouseSimple class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                    <span class="sr-only">{{ t("nav.home") }}</span>
                </LocaleLink>
            </li>
            <li v-if="props.project.id" class="flex items-center">
                <svg class="h-5 w-5 flex-shrink-0 text-gray-300" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                </svg>
                <LocaleLink :to="`/pathway/${props.project.id}`"
                    class="ml-2 text-sm font-medium text-gray-500 hover:text-gray-700">{{ props.project.title }}
                </LocaleLink>
            </li>
            <li class="flex items-center">
                <svg class="h-5 w-5 flex-shrink-0 text-gray-300" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                </svg>
                <LocaleLink :to="`/group/edit/${props.groupId}`">
                    <svg :class="[props.groupId === route.params.id as string
                            ? 'text-kashmir-500'
                            : 'text-gray-300', 'h-5 w-5 flex-shrink-0']"
                        fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <circle cx="10" cy="10" r="6" />
                    </svg>
                </LocaleLink>
            </li>
            <li v-if="props.themes && props.themes.length" v-for="o in props.themes" :key="`step-${o.id}`" class="flex items-center">
                <LocaleLink :to="`/journey/${props.groupId}/${o.id}`">
                    <svg :class="[o.id === route.params.id as string
                            ? 'text-kashmir-500'
                            : 'text-gray-300', 'h-5 w-5 flex-shrink-0']"
                        fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                        <circle cx="10" cy="10" r="6" />
                    </svg>
                </LocaleLink>
            </li>
        </ol>
    </nav>
</template>

<script setup lang="ts">
import { PhHouseSimple } from "@phosphor-icons/vue"
import { ISummary } from "@/interfaces"

const { t } = useI18n()
const route = useRoute()
const props = defineProps<{
    project: ISummary,
    groupId: string,
    themes: ISummary[]
}>()
</script>