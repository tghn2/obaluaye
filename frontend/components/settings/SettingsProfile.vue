<template>
    <div class="w-full">
        <div class="space-y-6 bg-white py-6 px-4 sm:p-6">
            <div>
                <h3 class="text-lg font-medium leading-6 text-gray-900">{{ t("settings.account.title") }}</h3>
            </div>
            <!-- <GuidepathStartPersonalJourney v-if="!authStore.completedPathway" /> -->
            <div class="space-y-1 grid grid-cols-1 gap-x-3 gap-y-4 sm:grid-cols-6">
                <div v-if="authStore.profile.full_name" class="sm:col-span-5">
                    <div class="block text-sm font-semibold leading-6 text-gray-900">
                        {{ t("settings.account.profileName") }}
                    </div>
                    <div class="block text-sm leading-6 text-gray-900">
                        {{ authStore.profile.full_name }}
                    </div>
                </div>
                <div v-if="authStore.profile.language" class="sm:col-span-1">
                    <div class="block text-sm font-semibold leading-6 text-gray-900 -mt-1">
                        {{ t("group.field.language") }}
                    </div>
                    <div class="block text-sm leading-6 text-gray-900">
                        <CommonLocaleView :language="authStore.profile.language" />
                    </div>
                </div>
                <div class="col-span-full">
                    <div class="block text-sm font-semibold leading-6 text-gray-900">
                        {{ t("settings.account.email") }}
                    </div>
                    <div class="block text-sm leading-6 text-gray-900">
                        {{ authStore.profile.email }}
                    </div>
                </div>
                <div v-if="authStore.profile.description" class="col-span-full">
                    <div class="block text-sm font-semibold leading-6 text-gray-900">
                        {{ t("group.field.description") }}
                    </div>
                    <div class="block text-sm leading-6 text-gray-900">
                        {{ authStore.profile.description }}
                    </div>
                </div>
                <div v-if="authStore.profile.subjects && authStore.profile.subjects.length" class="col-span-full">
                    <div class="block text-sm font-semibold leading-6 text-gray-900">
                        {{ t("settings.field.subjects") }}
                    </div>
                    <div class="block text-sm leading-6 text-gray-900">
                        {{ authStore.profile.subjects.join(", ") }}
                    </div>
                </div>
                <div v-if="authStore.profile.country && authStore.profile.country.length" class="col-span-full">
                    <div for="group-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                        {{ t("group.field.country") }}
                    </div>
                    <div class="block text-sm leading-6 text-gray-900">
                        <CommonCountryView :current-country="authStore.profile.country" />
                    </div>
                </div>
                <div 
                    v-if="authStore.profile.collection && authStore.profile.collection.length"
                    v-for="collection in authStore.profile.collection"
                    :key="`profile-collection${collection.id}`"
                    class="col-span-full">
                    <div v-if="collection.selection && collection.selection.length">
                        <div for="group-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ collection.title }}
                        </div>
                        <div class="block text-sm leading-6 text-gray-900">
                            {{ collection.selection.map(({ term }) => term).join(", ") }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
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