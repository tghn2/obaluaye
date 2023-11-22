<template>
    <div>
        <div class="flex-auto">
            <div v-if="props.theme.description" class="py-1">
                <div class="mt-1 text-sm leading-6 text-gray-700 sm:mt-0">
                    {{ props.theme.description }}
                </div>
            </div>
            <div v-if="props.theme.subjects && props.theme.subjects.length" class="py-1">
                <div class="group inline-flex text-xs font-medium text-gray-700">
                    <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        {{ props.theme.subjects.join(", ") }}
                    </span>
                </div>
            </div>
            <div class="py-1">
                <div v-if="props.theme.country && props.theme.country.length"
                    class="group inline-flex text-xs font-medium text-gray-700 ml-3">
                    <PhGlobeHemisphereEast class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        <CommonCountryView :current-country="props.theme!.country" />
                    </span>
                </div>
            </div>
            <div v-if="props.theme.spatial" class="py-1">
                <div class="group inline-flex text-xs font-medium text-gray-700">
                    <PhNote class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        {{ props.theme.spatial }}
                    </span>
                </div>
            </div>
            <div v-if="props.theme.resources && props.theme.resources.length" class="py-1 text-sm">
                <ResourceViewDisclosureCard :resources="props.theme.resources" />
            </div>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PhTag, PhGlobeHemisphereEast, PhNote } from "@phosphor-icons/vue"
import { ITheme } from "@/interfaces"

const { t } = useI18n()

const props = defineProps<{
    theme: ITheme,
}>()
</script>