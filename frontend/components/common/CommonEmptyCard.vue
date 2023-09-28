<template>
    <div class="rounded-md bg-cerulean-50 p-4">
        <div class="flex">
            <div class="flex-shrink-0">
                <PhInfo class="h-5 w-5 text-cerulean-400" aria-hidden="true" />
            </div>
            <div class="ml-3 flex-1 md:flex md:justify-between">
                <p class="text-sm text-cerulean-700">{{ props.term }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhInfo } from "@phosphor-icons/vue"

const props = defineProps<{
    term: String
}>()
</script>