<template>
    <div class="min-w-full hover:bg-gray-100">
        <LocaleLink :to="`/group/${props.comment.group.id}`">
            <div class="flex justify-between">
                <div class="py-0.5 text-xs leading-5 text-gray-500">
                    <span v-if="props.comment.researcher && props.comment.researcher.full_name"
                        class="font-medium text-gray-900">
                        {{ props.comment.researcher.full_name }}
                    </span>
                    <span
                        v-if="props.comment.researcher && !props.comment.researcher.full_name && props.comment.researcher.email"
                        class="font-medium text-gray-900">
                        {{ props.comment.researcher.email }}
                    </span>
                    <br />
                    <time :datetime="props.comment.modified" class="py-0.5 text-gray-500">
                        {{ readableDate(props.comment.modified as string, true, settingStore.locale) }}
                    </time>
                </div>
                <div class="py-0.5 text-xs leading-5 text-gray-500 group flex items-center space-x-2">
                    <PhUsersThree class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="text-gray-900">{{ props.comment.group.title }}</span>
                </div>
            </div>
            <p class="text-sm leading-6 text-gray-500">{{ props.comment.content }}</p>
        </LocaleLink>
    </div>
</template>

<script setup lang="ts">
import { PhUsersThree } from "@phosphor-icons/vue"
import { useSettingStore } from "@/stores"
import { IComment } from "@/interfaces"
import { readableDate } from "@/utilities"

const settingStore = useSettingStore()
const props = defineProps<{
    comment: IComment
}>()
</script>