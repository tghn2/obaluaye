<template>
    <div class="sm:px-6 sm:py-2 lg:px-8">
        <div
            class="flex items-center justify-between gap-x-6 ring-1 ring-kashmir-500 px-6 py-2.5 sm:rounded-xl sm:py-3 sm:pl-4 sm:pr-3.5">
            <p class="text-sm leading-6 text-gray-900">
                {{ t("pathway.journey.startResearch") }}
            </p>
            <button @click.prevent="submit"
                class="group flex items-center gap-x-1 text-sm leading-6 font-semibold text-white rounded-md p-1 pr-2 bg-kashmir-600 hover:bg-kashmir-800">
                <PhPlay class="h-4 w-4" aria-hidden="true" />
                <span>{{ t("pathway.journey.start") }}</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPlay } from "@phosphor-icons/vue"
import { useTokenStore, useToastStore, useSettingStore } from "@/stores"
import { apiGroup } from "@/api"
import { IGroup } from "@/interfaces"

const { t } = useI18n()
const localePath = useLocalePath()
const tokenStore = useTokenStore()
const toastStore = useToastStore()
const settingStore = useSettingStore()
const props = defineProps<{
    pathwayId: string,
    pathwayTitle: string,
}>()

async function submit() {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
        try {
            const data: IGroup = {
                title: `${t("pathway.journey.groupFor")} ${props.pathwayTitle}`,
                language: settingStore.locale
            }
            const { data: response } = await apiGroup.createTerm(tokenStore.token, props.pathwayId, data)
            if (response.value) {
                return await navigateTo(localePath(`/group/${response.value.msg}`))
            } else {
                toastStore.addNotice({
                    title: t("group.alert.createErrorTitle"),
                    content: t("group.alert.createErrorContent"),
                    icon: "error"
                })
            }
        } catch (error) {
            toastStore.addNotice({
                title: t("group.alert.createErrorTitle"),
                content: t("group.alert.createErrorContent"),
                icon: "error"
            })
        }
    }
}
</script>