<template>
    <main class="flex min-h-full">
        <div class="flex flex-1 flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
            <div class="mx-auto w-full max-w-sm lg:w-96">
                <div>
                    <PhEnvelopeSimple class="text-kashmir-500 h-12 w-12" aria-hidden="true" />
                    <h2 class="mt-6 text-3xl font-bold tracking-tight text-gray-900">{{ t("loginpage.magic.title") }}</h2>
                    <p class="text-sm font-medium text-gray-600 mt-6">
                        {{ t("loginpage.magic.description1") }}
                    </p>
                    <p class="text-sm font-medium text-gray-600 mt-2">
                        {{ t("loginpage.magic.description2") }}
                    </p>
                </div>
                <LocaleLink to="/login?oauth=true" class="mt-8 flex">
                    <PhLinkSimple class="text-kashmir-500 h-4 w-4 mr-1" aria-hidden="true" />
                    <p class="text-sm text-kashmir-500 align-middle">
                        {{ t("loginpage.magic.alternative") }}
                    </p>
                </LocaleLink>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import { PhLinkSimple, PhEnvelopeSimple } from "@phosphor-icons/vue"
import { useTokenStore } from "@/stores"
import { tokenParser } from "@/utilities"

definePageMeta({
    layout: "authentication",
    middleware: ["anonymous"],
});

const { t } = useI18n()
const localePath = useLocalePath()
const tokenStore = useTokenStore()
const redirectRoute = "/login"


onMounted(async () => {
    if (!tokenParser(tokenStore.token).hasOwnProperty("fingerprint")) {
        return await navigateTo(localePath(redirectRoute))
    }
})
</script>