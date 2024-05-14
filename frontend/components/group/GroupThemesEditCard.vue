<template>
    <div class="w-full">
        <div class="p-2">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div v-for="theme in props.themes" :key="theme.id" 
                    class="relative flex items-center space-x-3 rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm focus-within:ring-2 focus-within:ring-kashmir-500 focus-within:ring-offset-2 hover:border-gray-400">
                <div class="flex-shrink-0">
                    <span class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full border-2 border-kashmir-600">
                        <span class="text-kashmir-600">{{ theme.order as number + 1 }}</span>
                    </span>
                </div>
                <div class="min-w-0 flex-1">
                    <LocaleLink :to="`/journey/${props.groupId}/${theme.id}`" class="focus:outline-none">
                    <span class="absolute inset-0" aria-hidden="true" />
                    <p class="text-sm font-medium text-gray-700">{{ theme.title }}</p>
                    <div v-if="theme.subjects && theme.subjects.length" class="py-1">
                        <div class="group inline-flex text-xs font-medium text-gray-500">
                            <PhTag class="text-gray-500 h-4 w-4 shrink-0" aria-hidden="true" />
                            <span class="ml-1">
                                {{ theme.subjects.join(", ") }}
                            </span>
                        </div>
                    </div>
                    </LocaleLink>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhTag } from "@phosphor-icons/vue"
import { ISummary } from "@/interfaces"

const props = defineProps<{
    groupId: string,
    themes: ISummary[]
}>()
</script>