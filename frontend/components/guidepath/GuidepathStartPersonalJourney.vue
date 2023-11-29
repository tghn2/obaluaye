<template>
    <div class="sm:px-6 sm:py-2 lg:px-8">
        <div
            class="flex items-center justify-between gap-x-6 ring-1 ring-spring-500 px-6 py-2.5 sm:rounded-xl sm:py-3 sm:pl-4 sm:pr-3.5">
            <p class="text-sm leading-6 text-gray-900">
                {{ t("pathway.journey.startPersonal") }}
            </p>
            <button @click.prevent="submit"
                class="group flex items-center gap-x-1 text-sm leading-6 font-semibold text-white rounded-md p-1 px-1 bg-spring-500 hover:bg-spring-700">
                <PhPlay class="h-4 w-4" aria-hidden="true" />
                <span>{{ t("pathway.journey.start") }}</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPlay } from "@phosphor-icons/vue"
import { useToastStore} from "@/stores"
import { usePathwayStore } from "@/stores"

const { t } = useI18n()
const localePath = useLocalePath()
const pathwayStore = usePathwayStore()
const toastStore = useToastStore()

async function submit() {
    await pathwayStore.getPersonalTerm()
    if (pathwayStore.termPersonal) {
            toastStore.addNotice({
            title: t("group.alert.createSuccessTitle"),
            content: t("group.alert.createSuccessContent"),
            icon: "success"
        })
        return await navigateTo(localePath(`/journey/${pathwayStore.termPersonal}`))
    }
}
</script>