<template>
    <div class="sticky top-0 z-20 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white/75 sm:gap-x-6">
        <div class="flex w-full items-center justify-between gap-x-6 pb-2">
            <div class="flex items-center justify-left w-full space-x-4 truncate">
                <component :is="icons[props.purpose.toUpperCase()]"
                    class="h-7 w-7 m-2 flex-none rounded-full ring-1 ring-offset-4 ring-gray-400 text-gray-700 bg-white"
                    aria-hidden="true" />
                <h1 class="truncate text-lg font-semibold leading-7 text-gray-900">
                    {{ props.purpose }}: {{ props.title }}
                </h1>
            </div>
            <div class="flex flex-inline items-center space-x-2">
                <!-- Separator -->
                <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />
                <Menu as="div" class="relative inline-block text-left">
                    <div>
                        <MenuButton
                            class="inline-flex items-center w-full justify-center -ml-px gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                            <PhWarningCircle class="md:-ml-0.5 h-4 w-4 text-cerise-600" aria-hidden="true" />
                            <span class="hidden md:block">{{ t("header.reset") }}</span>
                            <PhCaretDown class="md:-ml h-4 w-4 text-gray-400" aria-hidden="true" />
                        </MenuButton>
                    </div>
                    <transition enter-active-class="transition ease-out duration-100"
                        enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
                        leave-active-class="transition ease-in duration-75"
                        leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                        <MenuItems
                            class="absolute right-0 z-30 mt-2 w-48 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                            <div class="py-1">
                                <MenuItem v-slot="{ active }">
                                <button type="button" @click.prevent="watchEditRequest('reset')"
                                    :class="[active ? 'bg-cerise-100 text-gray-900' : 'text-gray-700', 'flex items-center w-full gap-x-1.5 px-4 py-2 text-sm']">
                                    <PhArrowsClockwise class="-ml-0.5 h-5 w-5 text-gray-400" aria-hidden="true" />
                                    {{ t("header.reset") }}
                                </button>
                                </MenuItem>
                            </div>
                        </MenuItems>
                    </transition>
                </Menu>
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
import { Menu, MenuButton, MenuItems, MenuItem } from "@headlessui/vue"
import {
    PhArrowsClockwise, PhUpload, PhPath, PhCaretDown, PhWarningCircle, PhX
} from "@phosphor-icons/vue"
import { IKeyable } from "@/interfaces"

const { t } = useI18n()
const props = defineProps<{
    purpose: string,
    title: string,
    approach?: string,
}>()
const saveApproach = shallowRef("Save")
const icons: IKeyable = {
    PATHWAY: PhPath,
}
const emit = defineEmits<{ setEditRequest: [request: string] }>()

async function watchEditRequest(request: string) {
    // One of 'reset, 'cancel', 'save'
    emit("setEditRequest", request)
}

onMounted(async () => {
    if (props.approach) saveApproach.value = props.approach
})
</script>