<template>
    <main class="flex min-h-full">
        <div class="flex flex-1 flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
            <div class="mx-auto w-full max-w-sm lg:w-96">
                <div>
                    <h2 class="mt-6 text-3xl font-bold tracking-tight text-gray-900">{{ t("loginpage.reset.title") }}</h2>
                </div>
                <div class="mt-8">
                    <div class="mt-6">
                        <Form @submit="submit" :validation-schema="schema" class="space-y-6">
                            <div>
                                <label for="password" class="block text-sm font-medium text-gray-700">{{ t("loginpage.reset.passwordLabel") }}</label>
                                <div class="mt-1 group relative inline-block w-full">
                                    <Field id="password" name="password" type="password" autocomplete="password"
                                        class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-kashmir-600 focus:outline-none focus:ring-kashmir-600 sm:text-sm" />
                                    <ErrorMessage name="password"
                                        class="absolute left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
                                </div>
                            </div>

                            <div class="space-y-1">
                                <label for="confirmation" class="block text-sm font-medium text-gray-700">
                                    {{ t("loginpage.reset.passwordConfirm") }}
                                </label>
                                <div class="mt-1 group relative inline-block w-full">
                                    <Field id="confirmation" name="confirmation" type="password" autocomplete="confirmation"
                                        class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-kashmir-600 focus:outline-none focus:ring-kashmir-600 sm:text-sm" />
                                    <ErrorMessage name="confirmation"
                                        class="absolute left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
                                </div>
                            </div>
                            <div>
                                <button type="submit"
                                    class="flex w-full justify-center rounded-md border border-transparent bg-kashmir-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-kashmir-700 focus:outline-none focus:ring-2 focus:ring-kashmir-600 focus:ring-offset-2">
                                    {{ t("loginpage.submit") }}
                                </button>
                            </div>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores"

definePageMeta({
    layout: "authentication",
    middleware: ["anonymous"],
});

const { t } = useI18n()
const localePath = useLocalePath()
const schema = {
    password: { required: true, min: 8 },
    confirmation: { required: true, confirmed: "password" }
}
const authStore = useAuthStore()
const route = useRoute()
const redirectRoute = "/login"

async function submit(values: any) {
    await authStore.resetPassword(values.password, route.query.token as string)
    await new Promise((resolve) => {
        setTimeout(() => {
            resolve(true)
        }, 2000)
    })
    return await navigateTo(localePath(redirectRoute))
}

onMounted(async () => {
    // Check if token exists
    if (!route.query || !route.query.token) await navigateTo(localePath("/"))
})

</script>