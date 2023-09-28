<template>
    <div class="min-w-full hover:bg-gray-100">
        <LocaleLink :to="`/pathway/${props.pathway.id}`">
            <div class="flex w-full items-center">
                <div class="flex-1">
                    <div class="flex justify-between gap-x-4">
                        <div class="py-0.5 text-sm leading-5 text-gray-500">
                            <h2 class="font-bold text-gray-900">{{ props.pathway.title }}</h2>
                        </div>
                        <ul role="list" class="flex flex-row justify-end text-xs leading-5 py-0.5">
                            <li class="relative group flex flex-row text-xs font-medium text-gray-500 gap-x-1 pl-2">
                                <PhFlask v-if="props.pathway.pathType === 'RESEARCH'" class="text-gray-700 h-4 w-4 shrink-0"
                                    aria-hidden="true" />
                                <PhUser v-else class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                                {{ props.pathway.pathType }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <p v-if="props.pathway.description" class="text-sm leading-6 text-gray-500">{{ props.pathway.description }}</p>
            <div class="flex items-center justify-between">
                <div class="group flex flex-row text-xs font-medium text-gray-700">
                    <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span v-if="props.pathway.subjects && props.pathway.subjects.length" class="ml-1">
                        {{ props.pathway.subjects.join(", ") }}
                    </span>
                    <span v-else class="ml-1">
                        untagged
                    </span>
                </div>
                <ul role="list" class="flex flex-row justify-end text-xs">
                    <h3 id="detail-heading" class="sr-only">Pathway tasks and schema object</h3>
                    <li class="relative">
                        <LocaleLink :to="`/group/pathway/${props.pathway.id}`"
                            class="text-gray-700 hover:text-spring-600 group flex gap-x-1 p-2 font-semibold">
                            <PhUsers class="text-gray-700 group-hover:text-spring-600 h-4 w-4 shrink-0"
                                aria-hidden="true" />
                            <span class="hidden lg:block">Start</span>
                        </LocaleLink>
                    </li>
                </ul>
            </div>
        </LocaleLink>
    </div>
</template>

<script setup lang="ts">
import { PhCalendarBlank, PhFlask, PhUser, PhTag, PhUsers } from "@phosphor-icons/vue"
import { readableDate } from "@/utilities"
import { IPathway } from "@/interfaces"

const props = defineProps<{
    pathway: IPathway
}>()
</script>