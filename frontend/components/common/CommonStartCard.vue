<template>
    <div class="min-w-full">
        <div class="max-w-3xl mx-auto">
            <ul role="list" class="space-y-1">
                <li v-for="(start, startIdx) in launchAdmin" :key="startIdx">
                    <div v-if="start.show">
                        <div
                            class="relative flex items-center space-x-2 py-1 border border-gray-200 bg-white hover:bg-gray-100 rounded-md">
                            <div class="min-w-0 flex-auto">
                                <div class="flex items-center gap-x-3 p-2">
                                    <div
                                        :class="[start.background, 'flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg']">
                                        <component :is="start.icon" class="h-5 w-5 text-white" aria-hidden="true" />
                                    </div>
                                    <h2 class="min-w-0 text-sm font-semibold leading-6 text-gray-900">
                                        <LocaleLink :to="start.to" class="flex gap-x-2">
                                            <span>{{ t(start.title) }}</span>
                                            <span class="absolute inset-0" />
                                        </LocaleLink>
                                    </h2>
                                </div>
                                <div class="ml-2 mb-2 flex items-center gap-x-2.5 text-sm leading-5 text-gray-700">
                                    <p>{{ t(start.description) }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
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
    PhUser,
} from "@phosphor-icons/vue"
import { useAuthStore } from "@/stores"

const { t } = useI18n()
const authStore = useAuthStore()

const launchAdmin = [
    {
        title: "start.pathwayTitle",
        description: "start.pathwayDescription",
        icon: PhPath,
        to: "/pathway",
        background: "bg-kashmir-500",
        show: authStore.profile.completedPersonalPathway,
    },
    {
        title: "start.groupTitle",
        description: "start.groupDescription",
        icon: PhUsersThree,
        to: "/",
        background: "bg-cerise-500",
        show: authStore.profile.completedPersonalPathway,
    },
    {
        title: "start.commentTitle",
        description: "start.commentDescription",
        icon: PhChatTeardropText,
        to: "/",
        background: "bg-spring-500",
        show: authStore.profile.completedPersonalPathway,
    },
    {
        title: "start.personalTitle",
        description: "start.personalDescription",
        icon: PhUser,
        to: "/",
        background: "bg-spring-500",
        personal: true,
        show: !authStore.profile.completedPersonalPathway,
    },
]
</script>