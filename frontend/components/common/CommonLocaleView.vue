<template>
    <span>{{ currentLocale.name }}</span>
</template>
  
<script setup lang="ts">
import { LocaleObject } from "@nuxtjs/i18n/dist/runtime/composables"

const { locales } = useI18n()
const supportedLocales = locales.value as Array<LocaleObject>
const currentLocale = shallowRef({} as LocaleObject)
const props = defineProps<{
    language: string,
}>()

async function setLocale(term: string) {
    currentLocale.value = await supportedLocales.find((l) => l.iso === term || l.code === term) as LocaleObject
}

onMounted(async () => {
    await setLocale(props.language)
})
</script>
  