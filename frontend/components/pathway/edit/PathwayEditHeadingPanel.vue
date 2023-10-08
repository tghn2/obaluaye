<template>
    <div class="sticky top-0 z-20 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white/75 sm:gap-x-6">
        <div class="flex w-full items-center justify-between gap-x-6 pb-2">
            <div class="flex items-center justify-left w-full space-x-4 truncate">
                <div class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-kashmir-500">
                    <PhPath class="h-5 w-5 text-white" aria-hidden="true" />
                </div>
                <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
                    {{ t(props.title) }}
                </h1>
            </div>
            <div class="flex flex-inline items-center space-x-2">
                <!-- Separator -->
                <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />
                <CommonLocaleDropdown :language="pathwayStore.draft.language as string"
                    @set-locale-select="watchLocaleSelect" :disabled="pathwayStore.savingDraft" />
                <button type="button" @click.prevent="watchEditRequest('cancel')"
                    class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                    :disabled="pathwayStore.savingDraft">
                    <PhX class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                    <span class="hidden md:block">{{ t("header.cancel") }}</span>
                </button>
                <button type="button" @click.prevent="watchEditRequest('save')"
                    class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                    :disabled="pathwayStore.savingDraft">
                    <svg v-if="pathwayStore.savingDraft" aria-hidden="true"
                        class="md:-ml-0.5 h-4 w-4 text-kashmir-200 animate-spin fill-white" viewBox="0 0 100 101"
                        fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                            fill="currentColor" />
                        <path
                            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                            fill="currentFill" />
                    </svg>
                    <PhUpload v-else class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                    <span v-if="pathwayStore.savingDraft" class="hidden md:block">{{ t("header.saving") }}</span>
                    <span v-else class="hidden md:block">{{ t("header.save") }}</span>
                </button>
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">
import { PhUpload, PhPath, PhX } from "@phosphor-icons/vue"
import { usePathwayStore } from "@/stores"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const props = defineProps<{
    title: string,
}>()
const emit = defineEmits<{ setEditRequest: [request: string] }>()

async function watchLocaleSelect(select: string) {
    await watchEditRequest(select)
}
async function watchEditRequest(request: string) {
    // One of 'reset, 'cancel', 'save', 'language'
    emit("setEditRequest", request)
}

onMounted(async () => {
    if (!pathwayStore.draft || !pathwayStore.draft.language) pathwayStore.setLanguageDraft(pathwayStore.settings.locale)
})
</script>