<template>
    <span>{{ countryList.join(', ') }}</span>
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
import { useSettingStore } from "@/stores"

const settingStore = useSettingStore()
const countryList = ref([] as string[])

const props = defineProps<{
    currentCountry: string[],
}>()

// WATCHERS
// watch(
//     () => settingStore.currentLocale, () => setCountryList(),
// )

// SETTERS
onMounted(async () => {
    setCountryList()
})

function setCountryList() {
    countryList.value = []
    for (const code of props.currentCountry) {
        countryList.value.push(countries.getName(code, settingStore.currentLocale, { select: "official" }))
    }
}

</script>