<template>
    <div class="mt-4 p-2">
        <div class="flex-auto">
            <div v-if="props.summary.description" class="py-1 sm:px-6">
                <div class="mt-1 text-sm leading-6 text-gray-700 sm:mt-0">
                    {{ props.summary.description }}
                </div>
            </div>
            <div v-if="props.summary.subjects && props.summary.subjects.length" class="py-1 sm:px-6">
                <div class="group inline-flex text-xs font-medium text-gray-700">
                    <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        {{ props.summary.subjects.join(", ") }}
                    </span>
                </div>
            </div>
            <div class="py-1 sm:px-6">
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
        </div>
        <div v-if="props.summary.spatial" class="py-1 sm:px-6">
            <div class="group inline-flex text-xs font-medium text-gray-700">
                <PhNote class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    {{ props.summary.spatial }}
                </span>
            </div>
        </div>
        <div v-if="props.summary.pathway" class="py-1 mt-1 sm:px-6 border-y border-gray-200 ">
            <div class="group inline-flex text-xs font-medium text-gray-700">
                <PhPath class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    {{ t("group.nav.pathway") }}
                </span>
            </div>
            <div class="-mt-5">
                <CommonSummaryCard :summary="props.summary.pathway" :pathway="true" />
            </div>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PhTag, PhGlobeHemisphereEast, PhTranslate, PhNote, PhPath } from "@phosphor-icons/vue"
import { IGroup } from "@/interfaces"

const { t } = useI18n()
const props = defineProps<{
    summary: IGroup
}>()
</script>