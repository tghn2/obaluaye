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
                    <div 
                        v-for="universal in collectionStore.multi" 
                        :key="`universal-selection=${universal.id}`" 
                        class="col-span-full">
                        <label for="group-country-values" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ universal.title }}
                        </label>
                        <div class="mt-1">
                            <CollectionSelectionPanel :collection="universal" :all-selections="selectionChoices" @set-selection="watchCollectionSelection" />
                        </div>
                        <p v-if="universal.isMulti" class="mt-1 text-sm leading-6 text-gray-500">
                            {{ t("collection.multi") }}
                        </p>
                        <p v-else class="mt-1 text-sm leading-6 text-gray-500">
                            {{ t("collection.one") }}
                        </p>
                    </div>
                    <div v-if="authStore.profile.password" class="col-span-full">
                        <label for="original" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.account.accountPassword") }}
                        </label>
                        <div class="mt-1 group relative inline-block w-full">
                            <Field id="original" name="original" type="password" autocomplete="password"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
                            <ErrorMessage name="original"
                                class="absolute z-10 left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
                        </div>
                    </div>
                    <div v-else class="col-span-full">
                        <label for="password" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.security.new") }}
                        </label>
                        <div class="mt-1 group relative inline-block w-full">
                            <Field id="password" name="password" type="password" autocomplete="password"
                                class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-kashmir-600 focus:outline-none focus:ring-kashmir-600 sm:text-sm" />
                            <ErrorMessage name="password"
                                class="absolute z-10 left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
                        </div>
                        <label for="confirmation" class="block text-sm font-semibold leading-6 text-gray-900">
                            {{ t("settings.security.repeat") }}
                        </label>
                        <div class="mt-1 group relative inline-block w-full">
                            <Field id="confirmation" name="confirmation" type="password" autocomplete="confirmation"
                                class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-kashmir-600 focus:outline-none focus:ring-kashmir-600 sm:text-sm" />
                            <ErrorMessage name="confirmation"
                                class="absolute z-10 left-5 top-5 translate-y-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm after:content-[''] after:absolute after:left-1/2 after:bottom-[100%] after:-translate-x-1/2 after:border-8 after:border-x-transparent after:border-t-transparent after:border-b-gray-700" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="pb-6 text-right sm:px-6">
                <nav class="flex items-center justify-between mb-14 px-4 sm:px-0">
                    <div class="-mt-px flex w-0 flex-1">
                        <button
                            class="pointer-events-none group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500"
                            :disabled="true">
                            <PhArrowLeft class="mr-3 h-5 w-5" aria-hidden="true" />
                            {{ t("pathway.journey.previous") }}
                        </button>
                    </div>
                    <div class="-mt-px flex w-0 flex-1 justify-end">
                        <div class="flex flex-inline items-center space-x-2">
                            <button v-if="authStore.profile.password" @click.prevent="skipToPathway"
                                class="group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500">
                                <span>{{ t("pathway.journey.next") }}</span>
                                <PhArrowRight class="ml-3 h-5 w-5" aria-hidden="true" />
                            </button>
                            <span v-if="authStore.profile.password" class="block h-5 mt-3 w-px bg-gray-900/10" aria-hidden="true" />
                            <button type="submit"
                                class="group inline-flex items-center pr-1 pt-4 text-sm font-medium text-gray-500 hover:text-kashmir-500">
                                <span v-if="goNext">{{ t("pathway.journey.saveNext") }}</span>
                                <span v-else>{{ t("pathway.journey.save") }}</span>
                                <PhArrowRight class="ml-3 h-5 w-5" aria-hidden="true" />
                            </button>
                        </div>
                    </div>
                </nav>
            </div>
        </Form>
    </div>
</template>

<script setup lang="ts">
import { PhArrowLeft, PhArrowRight } from "@phosphor-icons/vue"
import { useAuthStore, useCollectionStore } from "@/stores"
import { IUserProfileUpdate, IKeyable } from "@/interfaces"

const { t } = useI18n()
const localePath = useLocalePath()
const authStore = useAuthStore()
const collectionStore = useCollectionStore()
const profile = ref({} as IUserProfileUpdate)
const subjects = ref("")
const selectionChoices = ref([] as string[])
const goNext = ref(true)

const props = defineProps<{
    nextPage: string,
}>()

const schema = {
    original: { required: authStore.profile.password, min: 8, max: 64 },
    password: { required: !authStore.profile.password, min: 8, max: 64 },
    confirmation: { required: !authStore.profile.password, confirmed: "password" },
    full_name: { required: false },
    email: { email: true, required: true },
}

onMounted(() => {
    resetProfile()
})

function resetProfile() {
    if (props.nextPage === authStore.profile.id) goNext.value = false
    if (authStore.profile.selection_ids && authStore.profile.selection_ids.length)
        selectionChoices.value = [...authStore.profile.selection_ids]
    profile.value = {
        full_name: authStore.profile.full_name,
        email: authStore.profile.email,
        description: authStore.profile.description,
        subjects: authStore.profile.subjects,
        country: authStore.profile.country,
        spatial: authStore.profile.spatial,
        language: authStore.profile.language,
        selection_ids: [...selectionChoices.value],
    }
    if (authStore.profile.subjects && authStore.profile.subjects.length) subjects.value = authStore.profile.subjects.join(", ")
}

async function watchLocaleSelect(response: string) {
    profile.value.language = response
}

function watchCountrySelect(response: string[]) {
    profile.value.country = response
}

function watchCollectionSelection(response: IKeyable) {
    if (Object.hasOwn(response, "choices") && Object.hasOwn(response, "original")) {
        selectionChoices.value = selectionChoices.value.filter(i => !response.original.includes(i))
        selectionChoices.value = [...selectionChoices.value, ...response.choices]
        profile.value.selection_ids = [...selectionChoices.value]
    }
}

async function skipToPathway() {
    if (goNext.value) return await navigateTo(localePath(`/journey/${props.nextPage}`))
    else return await navigateTo(localePath("/settings"))
}

async function submit(values: any) {
    if (
        (authStore.profile.password && values.original)
        || (
            !authStore.profile.password
            && values.password
            && (values.password === values.confirmation)
        )
    ) {
        if (!authStore.profile.password) profile.value.password = values.password
        else profile.value.original = values.original
        if (subjects.value) profile.value.subjects = subjects.value.split(",").map((item: string) => item.trim())
        if (values.email) {
            profile.value.email = values.email
            if (values.full_name) profile.value.full_name = values.full_name
            await authStore.updateUserProfile({ ...profile.value })
            resetProfile()
            if (goNext.value) return await navigateTo(localePath(`/journey/${props.nextPage}`))
            else return await navigateTo(localePath("/settings"))
        }
    }
}
</script>