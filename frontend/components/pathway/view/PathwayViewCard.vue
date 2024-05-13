<template>
    <div class="flex-auto">
        <div v-if="props.pathway.description" class="py-1 pt-4">
            <div class="mt-1 text-sm leading-6 text-gray-600 sm:mt-0">
                {{ props.pathway.description }}
            </div>
        </div>
        <div v-if="props.pathway.subjects && props.pathway.subjects.length" class="py-1">
            <div class="group inline-flex text-xs font-medium text-gray-700">
                <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    {{ props.pathway.subjects.join(", ") }}
                </span>
            </div>
        </div>
        <div class="py-1">
            <div v-if="props.pathway.temporalStart || props.pathway.temporalEnd" class="py-1">
                <div class="group inline-flex text-xs font-medium text-gray-700">
                    <PhCalendarBlank class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <div class="ml-1">
                        <span v-if="props.pathway.temporalStart">
                            {{ readableDate(props.pathway.temporalStart, true, appSettings.locale) }}
                        </span>
                        <span v-if="props.pathway.temporalEnd">
                            &mdash; {{ readableDate(props.pathway.temporalEnd, true, appSettings.locale) }}
                        </span>
                    </div>
                </div>
            </div>
            <div v-if="props.pathway.language" class="group inline-flex text-xs font-medium text-gray-700">
                <PhTranslate class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    <CommonLocaleView :language="props.pathway.language" />
                </span>
            </div>
            <div v-if="props.pathway.country && props.pathway.country.length"
                class="group inline-flex text-xs font-medium text-gray-700 ml-3">
                <PhGlobeHemisphereEast class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    <CommonCountryView :current-country="props.pathway.country" />
                </span>
            </div>
            <div v-if="props.pathway.spatial" class="py-1">
                <div class="group inline-flex text-xs font-medium text-gray-700">
                    <PhNote class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        {{ props.pathway.spatial }}
                    </span>
                </div>
            </div>
            <div v-if="props.pathway.bibliographicCitation" class="py-1">
                <div class="group inline-flex text-xs text-gray-700">
                    <PhBookBookmark class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1 italic">
                        {{ props.pathway.bibliographicCitation }}
                    </span>
                </div>
            </div>
        </div>
        <div v-if="props.pathway.resources && props.pathway.resources.length" class="py-1 text-sm">
            <ResourceViewDisclosureCard :resources="props.pathway.resources" :start-open="false" />
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PhTag, PhGlobeHemisphereEast, PhTranslate, PhNote, PhCalendarBlank, PhBookBookmark } from "@phosphor-icons/vue"
import { IPathway } from "@/interfaces"
import { readableDate } from "@/utilities"
import { useSettingStore } from "@/stores"

const { t } = useI18n()
const appSettings = useSettingStore()
const props = defineProps<{
    pathway: IPathway,
}>()
</script>