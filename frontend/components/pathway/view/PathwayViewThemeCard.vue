<template>
    <div class="flex-auto mb-2 p-2 border-b border-gray-100">
        <Disclosure v-slot="{ open, close }">
            <DisclosureButton @click="disclosureWatcher(open, close)"
                class="w-full text-sm font-semibold text-gray-900 pb-2">
                <div class="flex justify-between px-4">
                    <h3>{{ props.theme.title }}</h3>
                    <PhCaretDown :class="open ? 'rotate-180 transform' : ''" class="h-5 w-5" />
                </div>
            </DisclosureButton>
            <DisclosurePanel class="text-sm text-gray-500">
                <div class="flex-auto rounded-lg">
                    <dl>
                        <div v-if="props.theme.description" class="py-1 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-900">{{ t("theme.field.description") }}</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{
                                props.theme.description }}
                            </dd>
                        </div>
                        <div v-if="props.theme.subjects && props.theme.subjects.length"
                            class="py-1 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-900">{{ t("theme.field.subjects") }}</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                                {{ props.theme.subjects.join(", ") }}
                            </dd>
                        </div>
                        <div v-if="props.theme.country && props.theme.country.length"
                            class="py-1 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-900">{{ t("theme.field.country") }}</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                                <CommonCountryView :current-country="props.theme.country" />
                            </dd>
                        </div>
                        <div v-if="props.theme.spatial" class="py-1 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-900">{{ t("theme.field.spatial") }}</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{
                                props.theme.spatial }}
                            </dd>
                        </div>
                        <div v-if="props.theme.language" class="py-1 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-900">{{ t("theme.field.language") }}</dt>
                            <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                                <CommonLocaleView :language="props.theme.language" />
                            </dd>
                        </div>
                        <div class="py-1 sm:px-6">
                            <h4 class="text-sm font-medium text-gray-900 mb-2">{{ t("theme.field.nodes") }}</h4>
                            <div v-for="node in theme.nodes" :key="`node-${node.id}`" class="divide-y divide-gray-100">
                                <PathwayViewNodeCard :node="node" />
                            </div>
                        </div>
                    </dl>
                </div>
            </DisclosurePanel>
        </Disclosure>
    </div>
</template>
  
<script setup lang="ts">
import { PhCaretDown } from "@phosphor-icons/vue"
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { usePathwayStore } from "@/stores"
import { ITheme } from "@/interfaces"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const toggleClose = ref({} as typeof ref | HTMLElement)
const openState = ref(false)

const props = defineProps<{
    theme: ITheme,
}>()

// WATCHERS
function disclosureWatcher(open: boolean, close: typeof ref | HTMLElement) {
    // `open` seems to be false if open and true of closed ...
    if (!open) {
        toggleClose.value = close
        openState.value = true
        pathwayStore.setActiveDraft(props.theme.id as string)
    } else {
        openState.value = false
        pathwayStore.setActiveDraft("")
    }
}

watch(() => pathwayStore.activeEdit, () => {
    // @ts-ignore
    if (openState.value && props.theme.id !== pathwayStore.activeDraft) toggleClose.value()
})
</script>