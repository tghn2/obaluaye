<template>
    <Listbox as="div">
        <div class="relative mt-2 w-36">
            <ListboxButton
                class="relative lg:w-full cursor-default rounded-md py-1.5 pr-10 text-left text-gray-900 focus:outline-none lg:focus:ring-2 lg:focus:ring-kashmir-500 sm:text-sm sm:leading-6">
                <span class="flex items-center">
                    <PhGlobeHemisphereWest class="h-6 w-6 flex-shrink-0 text-gray-400" aria-hidden="true" />
                    <span class="ml-3 font-semibold flex md:hidden lg:block">{{ currentLocale.name }}</span>
                </span>
                <span class="flex md:hidden lg:flex pointer-events-none absolute inset-y-0 right-0 ml-3 items-center pr-2">
                    <PhCaretUpDown class="h-5 w-5 text-gray-400" aria-hidden="true" />
                </span>
            </ListboxButton>
            <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
                leave-to-class="opacity-0">
                <ListboxOptions
                    class="absolute -translate-y-full -bottom-24 z-10 mt-1 max-h-56 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption as="template" v-for="loc in supportedLocales" :key="loc.code" :value="loc.code"
                        v-slot="{ active, selected }">
                        <li @click="onLocaleChanged(loc)"
                            :class="[active ? 'bg-kashmir-600 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                            <div class="flex items-center">
                                <span :class="[selected ? 'font-semibold' : 'font-normal', 'ml-3 block truncate']">{{
                                    loc.name }}</span>
                            </div>
                            <span v-if="selected"
                                :class="[active ? 'text-white' : 'text-kashmir-600', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                <PhCheck class="h-5 w-5" aria-hidden="true" />
                            </span>
                        </li>
                    </ListboxOption>
                </ListboxOptions>
            </transition>
        </div>
    </Listbox>
</template>
  
<script setup lang="ts">
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from "@headlessui/vue"
import { PhCheck, PhCaretUpDown, PhGlobeHemisphereWest } from "@phosphor-icons/vue"
import { LocaleObject } from "@nuxtjs/i18n/dist/runtime/composables"

const { locale, locales } = useI18n()
const supportedLocales = locales.value as Array<LocaleObject>
const switchLocalePath = useSwitchLocalePath()
const currentLocale = ref({} as LocaleObject)

// When the visitor selects a new locale, route to
// to the new locale's path e.g. /en-CA/foo → /ar-EG/foo
async function onLocaleChanged(term: LocaleObject) {
    currentLocale.value = term
    // switchLocalePath('ar-EG') will return Arabic equivalent
    // for the *current* URL path e.g. if we're at /en-CA/about,
    // switchLocalePath('ar-EG') will return '/ar-EG/about'
    return await navigateTo({ path: switchLocalePath(term.code) })
}

function setLocale(term: string) {
    currentLocale.value = supportedLocales.find((l) => l.iso === term || l.code === term) as LocaleObject
}

onMounted(async () => {
    setLocale(locale.value)
})
</script>
  