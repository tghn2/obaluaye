<template>
    <div class="flex-auto">
        <div v-if="props.summary.title" class="py-1">
            <LocaleLink v-if="props.pathway" :to="`/pathway/${props.summary.id}`"
                class="mt-1 text-sm font-bold leading-6 text-kashmir-700 hover:text-kashmir-500 sm:mt-0">
                {{ props.summary.title }}
            </LocaleLink>
            <div v-else class="mt-1 text-sm font-bold leading-6 text-gray-700 sm:mt-0">
                {{ props.summary.title }}
            </div>
        </div>
        <div v-if="props.summary.description" class="py-1">
            <div class="mt-1 text-sm leading-6 text-gray-600 sm:mt-0">
                {{ props.summary.description }}
            </div>
        </div>
        <div v-if="props.summary.subjects && props.summary.subjects.length" class="py-1">
            <div class="group inline-flex text-xs font-medium text-gray-700">
                <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    {{ props.summary.subjects.join(", ") }}
                </span>
            </div>
        </div>
        <div class="py-1">
            <div v-if="props.summary.language" class="group inline-flex text-xs font-medium text-gray-700">
                <PhTranslate class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    <CommonLocaleView :language="props.summary.language" />
                </span>
            </div>
            <div v-if="props.summary.country && props.summary.country.length"
                class="group inline-flex text-xs font-medium text-gray-700 ml-3">
                <PhGlobeHemisphereEast class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    <CommonCountryView :current-country="props.summary.country" />
                </span>
            </div>
        </div>
        <div v-if="props.summary.resources && props.summary.resources.length" class="py-1 text-sm">
            <ResourceViewDisclosureCard :resources="props.summary.resources" />
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PhTag, PhGlobeHemisphereEast, PhTranslate } from "@phosphor-icons/vue"
import { ISummary } from "@/interfaces"

const props = defineProps<{
    summary: ISummary,
    pathway: boolean,
}>()
</script>