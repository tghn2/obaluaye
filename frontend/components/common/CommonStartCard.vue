<template>
    <div class="min-w-full">
        <div class="max-w-3xl mx-auto">
            <ul role="list" class="space-y-1">
                <li v-for="(start, startIdx) in launchAdmin" :key="startIdx"
                    class="relative flex items-center space-x-2 py-1 border border-gray-200 bg-white hover:bg-gray-100 rounded-md">
                    <div class="min-w-0 flex-auto">
                        <div class="flex items-center gap-x-3 p-2">
                            <div
                                :class="[start.background, 'flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg']">
                                <component :is="start.icon" class="h-5 w-5 text-white" aria-hidden="true" />
                            </div>
                            <h2 class="min-w-0 text-sm font-semibold leading-6 text-gray-900">
                                <LocaleLink :to="start.to" class="flex gap-x-2">
                                    <span>{{ start.title }}</span>
                                    <span class="absolute inset-0" />
                                </LocaleLink>
                            </h2>
                        </div>
                        <div class="ml-2 mb-2 flex items-center gap-x-2.5 text-sm leading-5 text-gray-700">
                            <p>{{ start.description }}</p>
                        </div>
                    </div>
                    <PhCaretDoubleRight class="h-4 w-4 flex-none text-gray-900" aria-hidden="true" />
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup lang="ts">
import {
    PhChatTeardropText,
    PhUsersThree,
    PhPath,
    PhCaretDoubleRight
} from "@phosphor-icons/vue"


const launchAdmin = [
    {
        title: "Manage pathways",
        description: "Organise tasks or teams. Specify a schema for all tasks to use, & define who gets to do what.",
        icon: PhPath,
        to: "/pathway",
        background: "bg-spring-500",
    },
    {
        title: "Manage groups",
        description: "Review the list of recent activities.",
        icon: PhUsersThree,
        to: "/",
        background: "bg-rose-500",
    },
    {
        title: "Review your schedule",
        description: "See which tasks need to be started or reviewed.",
        icon: PhChatTeardropText,
        to: "/",
        background: "bg-teal-500",
    },
]
</script>