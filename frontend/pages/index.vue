<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-7xl mx-auto">
        <div class="isolate mb-10">
            <svg class="absolute inset-0 -z-10 h-full w-full stroke-gray-200 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]"
                aria-hidden="true">
                <defs>
                    <pattern id="0787a7c5-978c-4f66-83c7-11c213f99cb7" width="90" height="30" x="50%" y="-1"
                        patternUnits="userSpaceOnUse">
                        <path d="M.5 200V.5H200" fill="none" />
                    </pattern>
                </defs>
                <rect width="100%" height="100%" stroke-width="0" fill="url(#0787a7c5-978c-4f66-83c7-11c213f99cb7)" />
            </svg>
            <div v-if="authStore.loggedIn">
                <CommonStartCard />
            </div>
            <div v-else>
                <div class="relative py-12 sm:py-16">
                    <div class="mx-auto max-w-7xl px-6 lg:px-8">
                        <div class="mx-auto max-w-2xl text-center">
                            <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                                Placeholder
                            </h1>
                            <p class="mt-6 text-lg leading-8 text-gray-600">
                                Placeholder slogan.
                            </p>
                            <div class="mt-6 flex items-center justify-center gap-x-6">
                                <LocaleLink v-if="!authStore.loggedIn" to="/login"
                                    class="rounded-md bg-spring-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-spring-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-spring-600">
                                    Get started</LocaleLink>
                                <LocaleLink to="/about" class="text-sm font-semibold leading-6 text-gray-900">Learn more
                                    <span aria-hidden="true">→</span>
                                </LocaleLink>
                            </div>
                        </div>
                        <div class="mt-12 flow-root sm:mt-20">
                            <div
                                class="-m-2 rounded-xl bg-gray-900/5 p-2 ring-1 ring-inset ring-gray-900/10 lg:-m-4 lg:rounded-2xl lg:p-4">
                                <img class="rounded-md shadow-2xl ring-1 ring-gray-900/10"
                                    src="https://placehold.co/1600x800" alt="Placeholder alt" />
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Alternating Features -->
                <div class="mx-auto max-w-2xl px-4 sm:px-6 lg:max-w-5xl lg:px-8">
                    <div class="mx-auto max-w-3xl text-center">
                        <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                            Placeholder call to action
                        </h2>
                        <p class="mt-4 text-gray-500">Placeholder action summary</p>
                    </div>
                    <div class="mt-12 space-y-6">
                        <div v-for="(feature, featureIdx) in features" :key="feature.name"
                            class="flex flex-col-reverse lg:grid lg:grid-cols-12 lg:items-center lg:gap-x-4">
                            <div
                                :class="[featureIdx % 2 === 0 ? 'lg:col-start-1' : 'lg:col-start-5 xl:col-start-6', 'mt-6 lg:mt-0 lg:row-start-1 lg:col-span-8 xl:col-span-7']">
                                <h3 class="text-lg font-medium text-gray-900">{{ feature.name }}</h3>
                                <p class="mt-2 text-sm text-gray-500">{{ feature.description }}</p>
                            </div>
                            <div
                                :class="[featureIdx % 2 === 0 ? 'lg:col-start-9 xl:col-start-8' : 'lg:col-start-1', 'flex-auto lg:row-start-1 lg:col-span-4 xl:col-span-5']">
                                <div class="aspect-w-5 aspect-h-2 overflow-hidden rounded-lg bg-gray-100">
                                    <img :src="feature.imageSrc" :alt="feature.imageAlt"
                                        class="mb-[-12%] object-cover object-center" />
                                </div>
                                <div class="relative" aria-hidden="true">
                                    <div class="absolute -inset-x-0 bottom-0 bg-gradient-to-t from-white pb-[20%]" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { tokenIsTOTP } from "@/utilities"
import { useAuthStore, useSettingStore, useTokenStore } from "@/stores"

definePageMeta({
    layout: "home",
});

const localePath = useLocalePath()
const authStore = useAuthStore()
const settingsStore = useSettingStore()
const tokenStore = useTokenStore()
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
})

// https://github.com/nuxt/nuxt/issues/14766
// Issues related to referencing '~/assets/img/...'
const features = [
    {
        name: "Placeholder text 1",
        description: "Place holder description 1.",
        imageSrc: "https://placehold.co/800x320",
        imageAlt: "Placeholder alt",
    },
    {
        name: "Placeholder text 2",
        description: "Place holder description 2.",
        imageSrc: "https://placehold.co/800x320",
        imageAlt: "Placeholder alt",
    },
    {
        name: "Placeholder text 3",
        description: "Place holder description 3.",
        imageSrc: "https://placehold.co/800x320",
        imageAlt: "Placeholder alt",
    },
]

// METADATA - START
// https://nuxt.com/docs/getting-started/seo-meta
const title = "whyqd.com — more research, less wrangling"
const description = "Perform schema-to-schema transforms for interoperability and data reuse. Transform messy data into structured schemas using readable, auditable methods."
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