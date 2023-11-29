<template>
    <div class="w-full">
        <Form @submit="submit" :validation-schema="schema">
            <div class="space-y-6 bg-white py-6 px-4 sm:p-6">
                <div>
                    <h3 class="text-lg font-medium leading-6 text-gray-900">{{ t("settings.account.title") }}</h3>
                    <p class="mt-1 text-sm text-gray-500">
                        {{ t("settings.account.description") }}
                    </p>
                </div>
                <GuidepathStartPersonalJourney v-if="!authStore.completedPathway" />
                <div class="space-y-1 grid grid-cols-1 gap-x-3 gap-y-4 sm:grid-cols-6">
                    <div class="sm:col-span-5">
                        <label for="full_name" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.account.profileName") }}
                        </label>
                        <div class="mt-1 group relative inline-block w-full">
                            <Field id="full_name" name="full_name" type="string" v-model="profile.full_name"
                                class="block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            <ErrorMessage name="email"
                                class="absolute left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
                        </div>
                    </div>
                    <div class="sm:col-span-1">
                        <label for="group-language-values"
                            class="block text-sm font-semibold leading-6 text-gray-900 -mt-1">
                            {{ t("group.field.language") }}
                        </label>
                        <div class="mt-1 group relative inline-block w-full">
                            <CommonLocaleDropdown :language="profile.language as string"
                                @set-locale-select="watchLocaleSelect" />
                        </div>
                    </div>
                    <div class="col-span-full">
                        <label for="email" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.account.email") }}
                        </label>
                        <div class="mt-1 group relative inline-block w-full">
                            <Field id="email" name="email" type="email" autocomplete="email" v-model="profile.email"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            <ErrorMessage name="email"
                                class="absolute left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
                        </div>
                    </div>
                    <div class="col-span-full">
                        <label for="description" class="block text-sm font-semibold leading-6 text-gray-900">{{
                            t("group.field.description") }}</label>
                        <div class="mt-1">
                            <textarea id="description" name="description" rows="3" v-model="profile.description"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                        </div>
                        <p class="mt-1 text-sm leading-6 text-gray-500">
                            <span>{{ t("settings.help.description") }}</span>
                        </p>
                    </div>
                    <div class="col-span-full">
                        <label for="group-subject-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.field.subjects") }}
                        </label>
                        <div class="mt-1">
                            <input type="text" name="group-subject-values" id="group-subject-values" v-model="subjects"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                        </div>
                        <p class="mt-1 text-sm leading-6 text-gray-500">{{ t("settings.help.subjects") }}</p>
                    </div>
                    <div class="col-span-full">
                        <label for="group-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("group.field.country") }}
                        </label>
                        <div class="mt-1">
                            <CommonCountrySelect :initial-choices="profile.country" @set-select="watchCountrySelect" />
                        </div>
                        <p class="mt-1 text-sm leading-6 text-gray-500">
                            {{ t("settings.help.country") }}
                        </p>
                    </div>
                    <div class="col-span-full">
                        <label for="original" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.account.accountPassword") }}
                        </label>
                        <div class="mt-1 group relative inline-block w-full">
                            <Field id="original" name="original" type="password" autocomplete="password"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            <ErrorMessage name="original"
                                class="absolute left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
                        </div>
                        <p v-if="!authStore.profile.password" class="mt-1 text-sm leading-6 text-gray-500 font-bold">
                            {{ t("settings.account.passwordRequired") }}
                        </p>
                    </div>
                </div>
            </div>
            <div class="pb-6 text-right sm:px-6">
                <button type="submit"
                    :class="[authStore.profile.password ? 'bg-kashmir-500 hover:bg-kashmir-700 focus:outline-none focus:ring-2 focus:ring-kashmir-600 focus:ring-offset-2' : 'bg-kashmir-300', 'inline-flex justify-center rounded-md border border-transparent py-2 px-4 text-sm font-medium text-white shadow-sm']"
                    :disabled="!authStore.profile.password">
                    {{ t("settings.account.submit") }}
                </button>
            </div>
        </Form>
    </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores"
import { IUserProfileUpdate } from "@/interfaces"

const { t } = useI18n()
const authStore = useAuthStore()
const profile = ref({} as IUserProfileUpdate)
const subjects = ref("")

const schema = {
    original: { required: authStore.profile.password, min: 8, max: 64 },
    full_name: { required: false },
    email: { email: true, required: true },
}

onMounted(() => {
    resetProfile()
})

function resetProfile() {
    profile.value = {
        full_name: authStore.profile.full_name,
        email: authStore.profile.email,
        description: authStore.profile.description,
        subjects: authStore.profile.subjects,
        country: authStore.profile.country,
        spatial: authStore.profile.spatial,
        language: authStore.profile.language,
    }
    if (authStore.profile.subjects && authStore.profile.subjects.length) subjects.value = authStore.profile.subjects.join(", ")
}

async function watchLocaleSelect(response: string) {
    profile.value.language = response
}

function watchCountrySelect(response: string[]) {
    profile.value.country = response
}

async function submit(values: any) {
    if ((!authStore.profile.password && !values.original) ||
        (authStore.profile.password && values.original)) {
        if (values.original) profile.value.original = values.original
        if (subjects.value) profile.value.subjects = subjects.value.split(",").map((item: string) => item.trim())
        if (values.email) {
            profile.value.email = values.email
            if (values.full_name) profile.value.full_name = values.full_name
            await authStore.updateUserProfile({ ...profile.value })
            resetProfile()
        }
    }
}
</script>