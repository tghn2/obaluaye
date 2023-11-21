<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-7xl mx-auto">
        <div class="mb-10">
            <div class="relative py-12 sm:py-16">
                <div class="mx-auto max-w-7xl px-6 lg:px-8">
                    <div class="mx-auto max-w-2xl text-center">
                        <div class="inline-flex items-center">
                            <img class="h-28 sm:h-32 w-auto" src="/img/mark.svg" :alt="t('common.title')" />
                            <h1 class="text-2xl px-1 font-bold tracking-tight text-gray-900 sm:text-4xl">
                                {{ t("frontpage.title") }}
                            </h1>
                        </div>
                        <p class="mt-6 text-lg leading-8 text-gray-600">
                            {{ t("frontpage.description") }}
                        </p>
                        <div class="mt-6 flex items-center justify-center gap-x-6">
                            <LocaleLink v-if="!authStore.loggedIn" to="/login"
                                class="rounded-md bg-kashmir-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-kashmir-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kashmir-600">
                                {{ t("frontpage.getstarted") }}
                            </LocaleLink>
                            <LocaleLink to="/about" class="text-sm font-semibold leading-6 text-gray-900">
                                {{ t("frontpage.learnmore") }}
                                <span aria-hidden="true">→</span>
                            </LocaleLink>
                        </div>
                    </div>
                    <!-- Featured Pathway -->
                    <div v-if="pathwayStore.term && pathwayStore.term.title" class="mx-auto max-w-2xl mt-12 sm:mt-18">
                        <div class="mx-auto max-w-3xl text-center mb-8">
                            <h2 class="text-xl font-bold tracking-tight text-gray-900 sm:text-2xl">
                                {{ t("frontpage.pathwayTitle") }}
                            </h2>
                        </div>
                        <div class="flow-root">
                            <div
                                class="-m-2 rounded-xl bg-gray-900/5 p-2 ring-1 ring-inset ring-gray-900/10 lg:rounded-2xl lg:p-4">
                                <PathwayCard :pathway="pathwayStore.term" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Featured Groups -->
            <div v-if="groupStore.multi && groupStore.multi.length"
                class="mx-auto max-w-2xl px-4 sm:px-6 lg:max-w-5xl lg:px-8">
                <div class="mx-auto max-w-3xl text-center mb-8">
                    <h2 class="text-xl font-bold tracking-tight text-gray-900 sm:text-2xl">
                        {{ t("frontpage.groupTitle") }}
                    </h2>
                </div>
                <div class="mt-8 space-y-6">
                    <div v-for="featured in  groupStore.multi" :key="featured.id" class="flow-root space-y-8">
                        <div
                            class="-m-2 rounded-xl bg-gray-900/5 p-2 ring-1 ring-inset ring-gray-900/10 lg:rounded-2xl lg:p-4">
                            <SearchCard :group="featured" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { tokenIsTOTP } from "@/utilities"
import { useAuthStore, useSettingStore, useTokenStore, useGroupStore, usePathwayStore } from "@/stores"

definePageMeta({
    layout: "home",
});

const { t } = useI18n()
const localePath = useLocalePath()
const authStore = useAuthStore()
const settingsStore = useSettingStore()
const tokenStore = useTokenStore()
const pathwayStore = usePathwayStore()
const groupStore = useGroupStore()
const route = useRoute()
const redirectTOTP = "/totp"
const redirectAfterLogin = "/"

onMounted(async () => {
    settingsStore.setPageName("nav.home")
    if (authStore.loggedIn) console.log("Welcome back :)")
    else console.log("A hearty welcome :)")
    // Check if email is being validated
    if (route.query && route.query.magic) {
        // No idea: https://stackoverflow.com/q/74759799/295606
        await new Promise((resolve) => {
            setTimeout(() => {
                resolve(true)
            }, 100)
        })
        if (!authStore.loggedIn) await authStore.magicLogin(route.query.magic as string)
        if (tokenIsTOTP(tokenStore.token)) await navigateTo(localePath(redirectTOTP))
        else await navigateTo(localePath(redirectAfterLogin))
    }
    await pathwayStore.getFeaturedTerm()
    await groupStore.getFeaturedMulti()
})

// METADATA - START
// https://nuxt.com/docs/getting-started/seo-meta
const title = t("seo.title")
const description = t("seo.description")
useHead({
    title,
    meta: [{
        name: "description",
        content: description
    }]
})
useServerSeoMeta({
    title,
    ogTitle: title,
    description: description,
    ogDescription: description,
    ogImage: "https://whyqd.com/img/crosswalk.jpg"
})
// METADATA - END
</script>