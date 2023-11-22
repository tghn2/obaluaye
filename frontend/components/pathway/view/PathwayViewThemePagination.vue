<template>
    <nav class="flex items-center justify-between mb-14 px-4 sm:px-0">
        <div class="-mt-px flex w-0 flex-1">
            <button @click="watchDirection('back')"
                :class="[themeIdx === 0 ? 'pointer-events-none' : '', 'group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500']"
                :disabled="themeIdx === 0">
                <PhArrowLeft class="mr-3 h-5 w-5" aria-hidden="true" />
                {{ t("pathway.journey.previous") }}
            </button>
        </div>
        <div class="-mt-px flex w-0 flex-1 justify-end">
            <button @click="watchDirection('next')"
                :class="[themeIdx === props.lastPage ? 'pointer-events-none' : '', 'group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500']"
                :disabled="themeIdx === props.lastPage">
                <span >{{ t("pathway.journey.next") }}</span>
                <PhArrowRight class="ml-3 h-5 w-5" aria-hidden="true" />
            </button>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { PhArrowLeft, PhArrowRight } from "@phosphor-icons/vue"

const { t } = useI18n()
const props = defineProps<{
    lastPage: number,
}>()
const emit = defineEmits<{ setThemeIndex: [idx: number] }>()
const themeIdx = ref(0)

function watchDirection(direction: string) {
    if (direction === "next" && themeIdx.value < props.lastPage) themeIdx.value += 1
    if (direction === "back" && themeIdx.value > 0) themeIdx.value -= 1
    emit("setThemeIndex", themeIdx.value)
}
</script>