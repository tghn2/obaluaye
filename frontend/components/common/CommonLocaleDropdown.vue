<template>
    <Listbox as="div" class="relative inline-block text-left">
        <div>
            <ListboxButton
                class="inline-flex items-center w-full justify-center -ml-px gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                <PhGlobeHemisphereWest class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                <span v-if="commonLocale.name" class="hidden md:block">{{ commonLocale.name }}</span>
                <PhCaretDown class="md:-ml h-4 w-4 text-gray-400" aria-hidden="true" />
            </ListboxButton>
        </div>
        <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
            leave-to-class="opacity-0">
            <ListboxOptions
                class="absolute z-10 mt-1 max-h-56 w-30 overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                <ListboxOption as="template" v-for="loc in supportedLocales" :key="loc.code" :value="loc.code"
                    v-slot="{ active, selected }">
                    <li @click="watchLocaleSelect(loc)"
                        :class="[active ? 'bg-spring-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                        <div class="flex items-center">
                            <span :class="[selected ? 'font-semibold' : 'font-normal', 'ml-3 block truncate']">{{
                                loc.name }}</span>
                        </div>
                        <span v-if="selected"
                            :class="[active ? 'text-white' : 'text-spring-600', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                            <PhCheck class="h-5 w-5" aria-hidden="true" />
                        </span>
                    </li>
                </ListboxOption>
            </ListboxOptions>
        </transition>
    </Listbox>
</template>
  
<script setup lang="ts">
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from "@headlessui/vue"
import { PhCheck, PhCaretDown, PhGlobeHemisphereWest } from "@phosphor-icons/vue"
import { LocaleObject } from "@nuxtjs/i18n/dist/runtime/composables"

const { locales } = useI18n()
const supportedLocales = locales.value as Array<LocaleObject>
const commonLocale = shallowRef({} as LocaleObject)
const props = defineProps<{
    language: string,
}>()
const emit = defineEmits<{ setLocaleSelect: [select: string] }>()

function watchLocaleSelect(select: LocaleObject) {
    commonLocale.value = select
    emit("setLocaleSelect", select.code)
}

async function setLocale(term: string) {
    commonLocale.value = await supportedLocales.find((l) => l.iso === term || l.code === term) as LocaleObject
}

onMounted(async () => {
    await setLocale(props.language)
})
</script>
  