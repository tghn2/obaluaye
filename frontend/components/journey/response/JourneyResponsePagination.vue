<template>
    <nav class="flex items-center justify-between mb-14 px-4 sm:px-0">
        <div class="-mt-px flex w-0 flex-1">
            <button v-if="props.lastPage" @click="watchDirection('last')"
                :class="[props.lastPage ? '' : 'pointer-events-none', 'group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500']">
                <PhArrowLeft class="mr-3 h-5 w-5" aria-hidden="true" />
                {{ t("pathway.journey.previous") }}
            </button>
        </div>
        <div class="-mt-px flex w-0 flex-1 justify-end">
            <button @click="watchDirection('next')"
                :class="[props.nextPage || props.editing ? '' : 'pointer-events-none', 'group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500']">
                <span v-if="props.editing">
                    <span v-if="props.nextPage">{{ t("pathway.journey.saveNext") }}</span>
                    <span v-else>{{ t("pathway.journey.save") }}</span>
                </span>
                <span v-else>{{ t("pathway.journey.next") }}</span>
                <PhArrowRight class="ml-3 h-5 w-5" aria-hidden="true" />
            </button>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { PhArrowLeft, PhArrowRight } from "@phosphor-icons/vue"

const { t } = useI18n()
const props = defineProps<{
    nextPage: boolean,
    lastPage: boolean,
    editing: boolean,
}>()
const emit = defineEmits<{ setPageResponse: [direction: string] }>()

function watchDirection(direction: string) {
    emit("setPageResponse", direction)
}

</script>