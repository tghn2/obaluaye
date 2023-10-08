<template>
    <div>
        <ul role="list" class="mt-6 flex justify-between border-b border-t border-gray-200 py-6 md:px-12">
            <li v-for="(item, itemIdx) in items" :key="itemIdx">
                <LocaleLink :to="item.to" class="flex items-center space-x-2 rounded-lg hover:bg-gray-50 pr-1">
                    <div :class="[item.background, 'flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg']">
                        <component :is="item.icon" class="h-6 w-6 text-white" aria-hidden="true" />
                    </div>
                    <h3 class="text-sm font-bold text-gray-900">
                        {{ item.title }}
                    </h3>
                </LocaleLink>
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import {
    PhDownloadSimple,
} from "@phosphor-icons/vue"

const items = [
    {
        title: "Import data",
        icon: PhDownloadSimple,
        to: "/import",
        background: "bg-cerise-500",
    },
]
</script>