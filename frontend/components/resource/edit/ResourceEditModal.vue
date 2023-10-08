<template>
    <div>
        <button type="button" @click="openModal"
            class="rounded-full p-1 ring-1 ring-inset ring-kashmir-300 hover:bg-kashmir-50">
            <PhBookmarkSimple class="h-4 w-4 text-kashmir-400" aria-hidden="true" />
        </button>
        <TransitionRoot appear :show="isOpen" as="template">
            <Dialog as="div" @close="closeModal" class="relative z-30">
                <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100"
                    leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
                    <div class="fixed inset-0 bg-black bg-opacity-25" />
                </TransitionChild>
                <div class="fixed inset-0 overflow-y-auto">
                    <div class="flex min-h-full max-w-3xl mx-auto items-center justify-center">
                        <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95"
                            enter-to="opacity-100 scale-100" leave="duration-200 ease-in" leave-from="opacity-100 scale-100"
                            leave-to="opacity-0 scale-95">
                            <DialogPanel
                                class="w-full max-w-md transform overflow-hidden rounded-md bg-white p-6 text-left align-middle shadow-xl transition-all">
                                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                                    {{ t("resource.name") }}
                                </DialogTitle>
                                <form class="flex-auto mt-2">
                                    <div class="grid grid-cols-1 gap-x-2 gap-y-2 sm:grid-cols-6">
                                        <div class="sm:col-span-4">
                                            <label for="resource-title"
                                                class="block text-sm font-semibold leading-6 text-gray-900">{{
                                                    t("resource.field.title") }}</label>
                                            <div class="mt-1">
                                                <input type="text" name="resource-title" id="resource-title"
                                                    v-model="draft.title"
                                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                                            </div>
                                            <p v-if="pathwayStore.isTranslatingDraft"
                                                class="mt-1 text-sm leading-6 text-gray-500">
                                                {{ pathwayStore.draft.title }}
                                            </p>
                                        </div>
                                        <div class="sm:col-span-2">
                                            <label for="resource-title"
                                                class="block text-sm font-semibold leading-6 text-gray-900">{{
                                                    t("resource.field.type") }}</label>
                                            <div class="mt-1">
                                                <InputSelectResourceType name="resource-type" id="resource-type"
                                                    :initial-type="(draft.resourceType as IResourceType)"
                                                    @set-select="watchInputResourceType" />
                                            </div>
                                        </div>
                                        <div class="col-span-full">
                                            <label for="resource-content"
                                                class="block text-sm font-semibold leading-6 text-gray-900">
                                                <span v-if="draft.resourceType === 'MARKDOWN'">{{
                                                    t("resource.types.markdown") }}</span>
                                                <span v-if="draft.resourceType === 'WEBLINK'">{{ t("resource.types.weblink")
                                                }}</span>
                                            </label>
                                            <div class="mt-1">
                                                <textarea v-if="draft.resourceType === 'MARKDOWN'" id="resource-content"
                                                    name="resource-content" rows="3" v-model="draft.content"
                                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                                                <input v-if="draft.resourceType === 'WEBLINK'" type="text"
                                                    name="resource-content" id="resource-content" v-model="draft.content"
                                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                                            </div>
                                        </div>
                                    </div>
                                </form>
                                <div class="flex flex-inline items-center space-x-2 justify-end mt-4">
                                    <button type="button" @click="closeModal"
                                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                                        <PhX class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                                        <span class="hidden md:block">{{ t("resource.cancel") }}</span>
                                    </button>
                                    <button type="button" @click="emitResource"
                                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                                        <PhBookmarkSimple class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                                        <span class="hidden md:block">{{ t("resource.store") }}</span>
                                    </button>
                                </div>
                            </DialogPanel>
                        </TransitionChild>
                    </div>
                </div>
            </Dialog>
        </TransitionRoot>
    </div>
</template>
  
<script setup lang="ts">
import { PhX, PhBookmarkSimple } from "@phosphor-icons/vue"
import {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
} from "@headlessui/vue"
import { IResource, IResourceType } from "@/interfaces"
import { usePathwayStore } from "@/stores"
import { generateUUID } from "@/utilities"

const { t } = useI18n()
const isOpen = ref(false)
const pathwayStore = usePathwayStore()
const draft = ref({} as IResource)

const props = defineProps<{
    initialDraft: IResource,
}>()
const emit = defineEmits<{
    setDraft: [draft: IResource],
}>()

// WATCHERS
function watchInputResourceType(response: IResourceType) {
    draft.value.resourceType = response
}

function emitResource() {
    const response = setDraft({ ...draft.value })
    emit("setDraft", response)
    if (!props.initialDraft || Object.keys(props.initialDraft).length === 0) draft.value = {
        id: generateUUID(),
        resourceType: "WEBLINK",
        language: pathwayStore.languageDraft,
        pathway_id: pathwayStore.draft.id,
    }
    closeModal()
}

// SETTERS
function setDraft(response: IResource) {
    return response
}

function resetDraft() {
    if (props.initialDraft && Object.keys(props.initialDraft).length) draft.value = { ...props.initialDraft }
    else draft.value = {
        id: generateUUID(),
        resourceType: "WEBLINK",
        language: pathwayStore.languageDraft,
        pathway_id: pathwayStore.draft.id,
    }
}

onMounted(async () => {
    resetDraft()
})

// MODAL
function closeModal() {
    isOpen.value = false
}
function openModal() {
    isOpen.value = true
}
</script>
  