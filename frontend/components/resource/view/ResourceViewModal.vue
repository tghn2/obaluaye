<template>
    <div>
        <button type="button" @click="openModal"
            class="inline-flex items-center group text-xs font-medium text-kashmir-800 hover:text-kashmir-500">
            <span>{{ props.resource.title }}</span>
            <PhArticle class="ml-1 h-4 w-4" aria-hidden="true" />
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
                                <DialogTitle as="h3" class="text-base font-medium leading-6 text-gray-900">
                                    {{ props.resource.title }}
                                </DialogTitle>
                                <div class="flex-auto text-sm mt-2">
                                    {{ props.resource.content }}
                                </div>
                                <div class="flex flex-inline items-center space-x-2 justify-end mt-4">
                                    <button type="button" @click="closeModal"
                                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                                        <PhX class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                                        <span class="hidden md:block">{{ t("resource.cancel") }}</span>
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
import { PhX, PhArticle } from "@phosphor-icons/vue"
import {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
} from "@headlessui/vue"
import { IResource } from "@/interfaces"

const { t } = useI18n()
const isOpen = ref(false)

const props = defineProps<{
    resource: IResource,
}>()

// MODAL
function closeModal() {
    isOpen.value = false
}
function openModal() {
    isOpen.value = true
}
</script>
  