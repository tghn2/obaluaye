<template>
    <div class="px-2">
        <Disclosure v-slot="{ open, close }">
            <DisclosureButton class="w-full text-sm font-semibold text-gray-900 pb-2">
                <div class="flex justify-between px-4 mt-1 font-medium text-gray-900 bg-spring-50 border-t border-spring-200 p-2">
                    <h4>
                        {{ t("pathway.journey.resources") }}
                    </h4>
                    <PhCaretDown :class="open ? 'rotate-180 transform' : ''" class="h-5 w-5" />
                </div>
            </DisclosureButton>
            <DisclosurePanel class="text-xs text-gray-500">
                <ul class="mt-1">
                    <li v-for="resource in props.resources" :key="resource.id">
                        <dl v-if="resource.resourceType === 'WEBLINK'" class="px-2 py-1">
                            <a :href="resource.content" target="_blank"
                                class="inline-flex items-center group text-xs font-medium text-kashmir-800 hover:text-kashmir-600">
                                <span>{{ resource.title }}</span>
                                <PhArrowSquareOut class="ml-1 h-4 w-4" aria-hidden="true" />
                            </a>
                        </dl>
                        <dl v-if="resource.resourceType === 'MARKDOWN'" class="px-2 py-1">
                            <ResourceViewModal :resource="resource" />
                        </dl>
                    </li>
                </ul>
            </DisclosurePanel>
        </Disclosure>
    </div>
</template>  

<script setup lang="ts">
import { PhArrowSquareOut, PhCaretDown } from "@phosphor-icons/vue"
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue"
import { IResource } from "@/interfaces"

const { t } = useI18n()

const props = defineProps<{
    resources: IResource[],
}>()
</script>