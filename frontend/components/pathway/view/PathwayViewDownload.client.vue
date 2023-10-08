<template>
    <div class="flex items-center p-3 mt-3 -ml-2">
        <button @click="getDownload"
            class="text-sm font-medium text-gray-900 hover:text-kashmir-600 group flex gap-x-1 p-2">
            <PhDownloadSimple class="text-gray-700 group-hover:text-kashmir-600 h-5 w-5 shrink-0" aria-hidden="true" />
            <span class="hidden sm:block">{{ t("pathway.download") }}</span>
        </button>

    </div>
</template>

<script setup lang="ts">
import { PhDownloadSimple } from "@phosphor-icons/vue"
import { useToastStore, useSettingStore, usePathwayStore } from "@/stores"
import { apiPathway } from "@/api"

const { t } = useI18n()
const route = useRoute()
const pathwayStore = usePathwayStore()
const settingsStore = useSettingStore()
const toasts = useToastStore()
const mimeType = "application/json"

function returnDownload(response: any, fileName: string) {
    // https://stackoverflow.com/a/18197341/295606
    const a = document.createElement("a")
    const data = `data:${mimeType},${encodeURIComponent(JSON.stringify(response))}`
    a.href = data
    a.download = fileName
    a.type = mimeType
    a.style.display = "none"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
}

async function getDownload() {
    if (route.params.id) {
        try {
            const { data: response } = await apiPathway.getSchemaDownload(route.params.id as string, settingsStore.currentLocale)
            if (response.value) {
                return returnDownload(response.value, `${pathwayStore.term.name}-${settingsStore.currentLocale}.json`)
            }
        } catch (error) {
            toasts.addNotice({
                title: "Download error",
                content: error as string,
                icon: "error"
            })
        }
    }
}
</script>