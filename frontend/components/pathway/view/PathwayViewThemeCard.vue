<template>
    <div v-if="theme && theme.hasOwnProperty('title')">
        <div class="bg-gray-100 p-1">
            <div class="group inline-flex text-xs font-medium text-gray-700">
                <PhSwatches class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="ml-1">
                    {{ theme.title }}
                </span>
            </div>
        </div>
        <div class="flex-auto">
            <div v-if="theme.description" class="py-1">
                <div class="mt-1 text-sm leading-6 text-gray-700 sm:mt-0">
                    {{ theme.description }}
                </div>
            </div>
            <div v-if="theme.subjects && theme.subjects.length" class="py-1">
                <div class="group inline-flex text-xs font-medium text-gray-700">
                    <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        {{ theme.subjects.join(", ") }}
                    </span>
                </div>
            </div>
            <div class="py-1">
                <div v-if="theme.country && theme.country.length"
                    class="group inline-flex text-xs font-medium text-gray-700 ml-3">
                    <PhGlobeHemisphereEast class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        <CommonCountryView :current-country="theme!.country" />
                    </span>
                </div>
            </div>
            <div v-if="theme.spatial" class="py-1">
                <div class="group inline-flex text-xs font-medium text-gray-700">
                    <PhNote class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        {{ theme.spatial }}
                    </span>
                </div>
            </div>
            <div v-if="theme.resources && theme.resources.length" class="py-1 text-sm">
                <ResourceViewDisclosureCard :resources="theme.resources" />
            </div>
            <div v-for="node in theme.nodes" :key="`node-${node.id}`">
                <PathwayViewNodeCard :node="node" />
            </div>
        </div>
        <PathwayViewThemePagination :last-page="props.themes.length - 1"  @set-theme-index="watchThemeRequest" />
    </div>
</template>
  
<script setup lang="ts">
import { PhSwatches, PhTag, PhGlobeHemisphereEast, PhNote } from "@phosphor-icons/vue"
import { ITheme } from "@/interfaces"

const { t } = useI18n()
const theme = ref<ITheme>({})
const themeIdx = ref(0)
const themeIdxMax = ref(0)

const props = defineProps<{
    themes: ITheme[],
}>()

// WATCHERS
function watchThemeRequest(request: number) {
    if (!(theme.value && theme.hasOwnProperty('title')) || request !== themeIdx.value) {
        themeIdx.value = request
        theme.value = props.themes[themeIdx.value]
    }
}

onMounted(async () => {
    themeIdxMax.value = props.themes.length - 1
    watchThemeRequest(themeIdx.value)
})
</script>