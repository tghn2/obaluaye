<template>
    <div>
        <component v-if="props.check" :is="PhCheckCircle" class="text-green-600 flex-shrink-0 -ml-1 mr-3 h-6 w-6"
            aria-hidden="true" />
        <component v-else :is="PhXCircle" class="text-red-600 flex-shrink-0 -ml-1 mr-3 h-6 w-6" aria-hidden="true" />
    </div>
</template>

<script setup lang="ts">
import { PhCheckCircle, PhXCircle } from "@phosphor-icons/vue"

const props = defineProps({
    check: Boolean
})
</script>