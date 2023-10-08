<template>
    <button type="button"
        class="rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-kashmir-500 focus:ring-offset-2">
        <span class="sr-only">View notifications</span>
        <PhBellSimple class="h-6 w-6" aria-hidden="true" />
    </button>
</template>

  
<script setup lang="ts">
import { PhBellSimple } from "@phosphor-icons/vue"
</script>