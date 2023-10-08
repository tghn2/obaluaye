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
            </div>
            <div class="flex flex-inline items-center space-x-2">
                <!-- Separator -->
                <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />
                <button type="button" @click.prevent="watchEditRequest('cancel')"
                    class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                    <PhX class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                    <span class="hidden md:block">{{ t("header.cancel") }}</span>
                </button>
                <button type="button" @click.prevent="watchEditRequest('save')"
                    class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                    <PhUpload class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                    <span class="hidden md:block">{{ t("header.save") }}</span>
                </button>
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">
import { PhUpload, PhUsersThree, PhX } from "@phosphor-icons/vue"

const { t } = useI18n()
const props = defineProps<{
    title: string,
}>()
const emit = defineEmits<{ setEditRequest: [request: string] }>()

async function watchEditRequest(request: string) {
    // One of 'reset, 'cancel', 'save'
    emit("setEditRequest", request)
}
</script>