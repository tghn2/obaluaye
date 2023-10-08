<template>
    <Listbox v-model="choices" id="country-selection-codes" multiple>
        <div class="relative mt-1">
            <ListboxButton
                class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus-visible:border-kashmir-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-kashmir-300 sm:text-sm">
                <span v-if="choices && choices.length" class="block truncate text-gray-900">
                    {{ choices.map((choice) => countryList[choice]).join(', ') }}
                </span>
                <span v-else class="block truncate text-gray-500">
                    {{ t("form.select") }}
                </span>
                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <PhCaretUpDown class="h-5 w-5 text-gray-400" aria-hidden="true" />
                </span>
            </ListboxButton>
            <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                leave-to-class="opacity-0">
                <ListboxOptions
                    class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="code in countryCodes" :key="`country-code-${code}`"
                        :value="code" as="template">
                        <li :class="[
                            active ? 'bg-kashmir-100 text-kashmir-900' : 'text-gray-900',
                            'relative cursor-default select-none py-2 pl-10 pr-4',
                        ]">
                            <span :class="[
                                selected ? 'font-medium' : 'font-normal',
                                'block truncate',
                            ]">{{ countryList[code] }}</span>
                            <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-kashmir-600">
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
import countries from "i18n-iso-countries"
import english from "i18n-iso-countries/langs/en.json"
import french from "i18n-iso-countries/langs/fr.json"
import spanish from "i18n-iso-countries/langs/es.json"
import portuguese from "i18n-iso-countries/langs/pt.json"
countries.registerLocale(english)
countries.registerLocale(french)
countries.registerLocale(spanish)
countries.registerLocale(portuguese)

import { PhCaretUpDown, PhCheck } from "@phosphor-icons/vue"
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, } from "@headlessui/vue"
import { IKeyable } from "@/interfaces"
import { useSettingStore } from "@/stores"


const { t } = useI18n()
const settingStore = useSettingStore()
const countryList = ref({} as IKeyable)
const countryCodes = ref([] as string[])
const choices = ref([] as string[])

const props = defineProps<{
    initialChoices?: string[],
}>()
const emit = defineEmits<{
    setSelect: [select: string[]]
}>()

// WATCHERS
watch(
    () => settingStore.currentLocale, () => setCountryList(),
)

watch(
    () => choices.value, () => {
        emit("setSelect", choices.value)
    }
)


// SETTERS
onMounted(async () => {
    setCountryList()
    if (props.initialChoices && props.initialChoices.length) choices.value = [...props.initialChoices]
})

function setCountryList() {
    countryList.value = countries.getNames(settingStore.currentLocale, { select: "official" })
    countryCodes.value = Object.keys(countryList.value)
    countryCodes.value.sort((a, b) => countryList.value[a].localeCompare(countryList.value[b]))
}

</script>