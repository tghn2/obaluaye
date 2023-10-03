<template>
    <div class="flex-auto mb-2 p-2 border-b-2 border-spring-200">
        <Disclosure v-slot="{ open, close }">
            <DisclosureButton @click="disclosureWatcher(open, close)"
                class="w-full text-base font-semibold text-gray-900 pb-2">
                <div class="flex justify-between px-4">
                    <h2 v-if="draft.title">{{ draft.title }}</h2>
                    <h2 v-else class="text-gray-700 italic">New theme</h2>
                    <PhDotsSix v-if="props.initialDraft.id !== pathwayStore.activeDraft" class="h-5 w-5" />
                    <PhCaretDown :class="open ? 'rotate-180 transform' : ''" class="h-5 w-5" />
                </div>
            </DisclosureButton>
            <DisclosurePanel class="p-4 text-sm text-gray-500">
                <form class="flex-auto rounded-lg p-3">
                    <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
                        <div class="col-span-full">
                            <label for="theme-title" class="block text-sm font-semibold leading-6 text-gray-900">{{
                                t("theme.field.title") }}</label>
                            <div class="mt-2">
                                <input type="text" name="theme-title" id="theme-title" v-model="draft.title"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p v-if="pathwayStore.isTranslatingDraft" class="mt-2 text-sm leading-6 text-gray-500">
                                {{ props.initialDraft.title }}
                            </p>
                        </div>
                        <div class="col-span-full">
                            <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">{{
                                t("theme.field.description") }}</label>
                            <div class="mt-2">
                                <textarea id="description" name="description" rows="3" v-model="draft.description"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">
                                <span v-if="pathwayStore.isTranslatingDraft">{{ props.initialDraft.description }}</span>
                                <span v-else>{{ t("theme.help.description") }}</span>
                            </p>
                        </div>
                        <div class="col-span-full">
                            <label for="theme-subject-values" class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ t("theme.field.subjects") }}
                            </label>
                            <div class="mt-2">
                                <input type="text" name="theme-subject-values" id="theme-subject-values" v-model="subjects"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">{{ t("theme.help.subjects") }}</p>
                        </div>
                        <div class="col-span-full">
                            <label for="pathway-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ t("pathway.field.country") }}
                            </label>
                            <div class="mt-2">
                                <CommonCountrySelect :initial-choices="draft.country" @set-select="watchCountrySelect" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">
                                {{ t("pathway.help.country") }}
                            </p>
                        </div>
                        <div class="col-span-full">
                            <label for="theme-spatial-values" class="block text-sm font-semibold leading-6 text-gray-900">
                                {{ t("theme.field.spatial") }}
                            </label>
                            <div class="mt-2">
                                <input type="text" name="theme-spatial-values" id="theme-spatial-values"
                                    v-model="draft.spatial"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                            </div>
                            <p class="mt-2 text-sm leading-6 text-gray-500">
                                {{ t("theme.help.spatial") }}
                            </p>
                        </div>
                        <div class="col-span-full my-1 py-1 border-t border-gray-100">
                            <PathwayEditResourceCard :initial-drafts="draft.resources" @set-drafts="watchResourcesUpdate" />
                        </div>
                    </div>
                </form>
            </DisclosurePanel>
        </Disclosure>
    </div>
</template>
  
<script setup lang="ts">
import { storeToRefs } from "pinia"
import { PhDotsSix, PhCaretDown } from "@phosphor-icons/vue"
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { usePathwayStore } from "@/stores"
import { ITheme, IResource } from "@/interfaces"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const { activeEdit, languageEdit } = storeToRefs(pathwayStore)
const toggleClose = ref({} as typeof ref | HTMLElement)
const openState = ref(false)
const draft = ref({} as ITheme)
const subjects = ref("")

const props = defineProps<{
    initialDraft: ITheme,
}>()
const emit = defineEmits<{
    setDraft: [draft: ITheme]
}>()

// WATCHERS
function disclosureWatcher(open: boolean, close: typeof ref | HTMLElement) {
    // `open` seems to be false if open and true of closed ...
    if (!open) {
        toggleClose.value = close
        openState.value = true
        pathwayStore.setActiveDraft(props.initialDraft.id as string)
    } else {
        openState.value = false
        pathwayStore.setActiveDraft("")
    }
}

function watchCountrySelect(response: string[]) {
    draft.value.country = response
}

function watchResourcesUpdate(update: IResource[]) {
    draft.value.resources = update
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
function setDraft(response: ITheme): ITheme {
    if (subjects.value) response.subjects = subjects.value.split(",").map((item: string) => item.trim())
    return response
}

function resetDraft() {
    draft.value = { ...props.initialDraft }
    if (draft.value.subjects && draft.value.subjects.length) subjects.value = draft.value.subjects.join(", ")
}

onMounted(async () => {
    resetDraft()
})

</script>