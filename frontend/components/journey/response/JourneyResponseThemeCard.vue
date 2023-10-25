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
            <div v-if="props.theme.resources && props.theme.resources.length" class="py-1">
                <h4 class="mt-1 text-sm font-medium text-gray-900 bg-spring-50 border-t border-spring-200 p-2">
                    {{ t("pathway.journey.resources") }}
                </h4>
                <ul class="mt-1">
                    <li v-for="resource in props.theme.resources" :key="resource.id">
                        <dl v-if="resource.resourceType === 'WEBLINK'" class="px-2 py-1">
                            <a :href="resource.content" target="_blank"
                                class="inline-flex items-center group test-sm font-medium text-kashmir-800 hover:text-kashmir-600">
                                <span>{{ resource.title }}</span>
                                <PhArrowSquareOut class="ml-1 h-4 w-4" aria-hidden="true" />
                            </a>
                        </dl>
                        <dl v-if="resource.resourceType === 'MARKDOWN'" class="px-2 py-1">
                            <ResourceViewModal :resource="resource" />
                        </dl>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PhArrowSquareOut, PhTag, PhGlobeHemisphereEast, PhTranslate, PhNote } from "@phosphor-icons/vue"
import { ITheme } from "@/interfaces"

const { t } = useI18n()

const props = defineProps<{
    theme: ITheme,
}>()
</script>