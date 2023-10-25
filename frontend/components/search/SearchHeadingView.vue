<template>
    <div class="sticky top-0 z-20 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white/75 sm:gap-x-6">
        <div class="flex w-full items-center justify-between gap-x-6 pb-2">
            <div class="flex items-center justify-left w-full space-x-4 truncate">
                <div class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-kashmir-500">
                    <PhUsersThree class="h-5 w-5 text-white" aria-hidden="true" />
                </div>
                <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
                    {{ props.title }}
                </h1>
                <PhChecks v-if="props.isComplete" class="text-spring-600 h-6 w-6 shrink-0" aria-hidden="true" />
                <PhFeather v-if="props.isFeatured" class="text-yellow-600 h-6 w-6 shrink-0" aria-hidden="true" />
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">
import { PhUsersThree, PhChecks, PhFeather } from "@phosphor-icons/vue"

const props = defineProps<{
    title: string,
    isComplete: boolean,
    isFeatured: boolean,
}>()
</script>