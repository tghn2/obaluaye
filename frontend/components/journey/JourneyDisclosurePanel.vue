<template>
    <div class="flex-auto mb-2 p-2 border-b-2 border-spring-200">
        <Disclosure v-slot="{ open, close }">
            <DisclosureButton @click="disclosureWatcher(open, close)"
                class="w-full text-base font-semibold text-gray-900 pb-2">
                <div v-if="props.initialDraft.id !== pathwayStore.activeDraft"
                    class="flex w-full justify-center items-center rounded-lg ">
                    <PhDotsSix :class="open ? 'rotate-90 transform' : ''" class="h-5 w-5" />
                </div>
                <div class="flex justify-between px-4">
                    <h2>Metadata</h2>
                    <PhCaretDown :class="open ? 'rotate-180 transform' : ''" class="h-5 w-5" />
                </div>
            </DisclosureButton>
            <DisclosurePanel class="p-4 text-sm text-gray-500">
                {{ draft }}
            </DisclosurePanel>
        </Disclosure>
    </div>
</template>
  
<script setup lang="ts">
import { storeToRefs } from "pinia"
import { PhDotsSix, PhCaretDown } from "@phosphor-icons/vue"
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { usePathwayStore } from "@/stores"
import { IKeyable } from "@/interfaces"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const { activeEdit, languageEdit } = storeToRefs(pathwayStore)
const toggleClose = ref({} as typeof ref | HTMLElement)
const openState = ref(false)
const draft = ref({} as IKeyable)

const props = defineProps<{
    initialDraft: IKeyable,
}>()
const emit = defineEmits<{ setDraft: [draft: IKeyable] }>()

// WATCHERS
function disclosureWatcher(open: boolean, close: typeof ref | HTMLElement) {
    // console.log("open", props.initialDraft.id, open)
    // `open` seems to be false if open and true of closed ...
    if (!open) {
        toggleClose.value = close
        openState.value = true
        pathwayStore.setActiveDraft(props.initialDraft.id)
    } else {
        openState.value = false
        pathwayStore.setActiveDraft("")
    }
}

watch(() => pathwayStore.activeEdit, () => {
    // @ts-ignore
    if (openState.value && props.initialDraft.id !== pathwayStore.activeDraft) toggleClose.value()
})

watch(
    () => draft.value, () => {
        const response = setDraft({ ...draft.value })
        emit("setDraft", response)
    },
    { deep: true }
)

// SETTERS
function setDraft(response: IKeyable): IKeyable {
    return response
}

function resetDraft() {
    draft.value = { ...props.initialDraft }
}

onMounted(async () => {
    resetDraft()
})
</script>