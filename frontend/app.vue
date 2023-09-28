<template>
    <div>

        <Head>
            <Link rel="icon" href="/favicon.ico" sizes="any" />
            <Link rel="icon" href="/favicon.svg" type="image/svg+xml" />
            <Link rel="apple-touch-icon" href="/apple-touch-icon-180x180.png" />
        </Head>
        <div class="h-full">
            <VitePwaManifest />
            <NuxtLoadingIndicator />
            <NuxtLayout>
                <NuxtPage />
            </NuxtLayout>
        </div>
    </div>
</template>

<script setup lang="ts">
// https://stackoverflow.com/a/76477511/295606
const { locale } = useI18n()
import { useSettingStore } from "@/stores"

const settingStore = useSettingStore()

watch(
    () => locale.value,
    (value) => settingStore.setCurrentLocale(value),
);

</script>