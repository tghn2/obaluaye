<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done' && pathwayStore.term && pathwayStore.term.name">
            <CommonHeadingView purpose="Pathway" :title="pathwayStore.term.title as string"
                @set-edit-request="watchHeadingRequest" />
            <dl class="divide-y divide-gray-100">
                <div v-if="pathwayStore.term.title" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-900">{{ t("pathway.field.title") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{
                        pathwayStore.term.title }}</dd>
                </div>
                <div v-if="pathwayStore.term.description" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-900">{{ t("pathway.field.description") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{
                        pathwayStore.term.description }}
                    </dd>
                </div>
                <div v-if="pathwayStore.term.subjects && pathwayStore.term.subjects.length"
                    class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-900">{{ t("pathway.field.subjects") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                        {{ pathwayStore.term.subjects.join(", ") }}
                    </dd>
                </div>
                <div v-if="pathwayStore.term.country && pathwayStore.term.country.length"
                    class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-900">{{ t("pathway.field.country") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                        <CommonCountryView :current-country="pathwayStore.term.country" />
                    </dd>
                </div>
                <div v-if="pathwayStore.term.spatial" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-900">{{ t("pathway.field.spatial") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{
                        pathwayStore.term.spatial }}
                    </dd>
                </div>
                <div v-if="pathwayStore.term.temporalStart || pathwayStore.term.temporalEnd"
                    class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-900">{{ t("pathway.field.temporal") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                        <span v-if="pathwayStore.term.temporalStart">{{
                            readableDate(pathwayStore.term.temporalStart) }}</span>
                        &mdash;
                        <span v-if="pathwayStore.term.temporalEnd">{{
                            readableDate(pathwayStore.term.temporalEnd) }}</span>
                    </dd>
                </div>
                <div v-if="pathwayStore.term.language" class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-900">{{ t("pathway.field.language") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                        <CommonLocaleView :language="pathwayStore.term.language" />
                    </dd>
                </div>
                <div v-if="pathwayStore.term.bibliographicCitation"
                    class="px-4 py-2 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt class="text-sm font-medium text-gray-900">{{ t("pathway.field.citation") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                        {{ pathwayStore.term.bibliographicCitation }}
                    </dd>
                </div>
            </dl>
        </div>
    </div>
</template>

<script setup lang="ts">
import { readableDate } from "@/utilities"
import { useSettingStore, usePathwayStore } from "@/stores"

const { t } = useI18n()
const appSettings = useSettingStore()
const route = useRoute()
const pathwayStore = usePathwayStore()

async function watchHeadingRequest(request: string) {
    switch (request) {
        case "remove":
            await pathwayStore.removeTerm(route.params.id as string)
            return await navigateTo("/pathway")
        case "edit":
            return await navigateTo(`/pathway/edit/${route.params.id}`)
    }
}

onMounted(async () => {
    appSettings.setPageName("nav.pathways")
    await pathwayStore.getTerm(route.params.id as string)
    if (!pathwayStore.term || Object.keys(pathwayStore.term).length === 0)
        throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
})

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