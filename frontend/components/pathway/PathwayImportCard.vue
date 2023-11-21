<template>
    <div class="mt-6 flex justify-center space-x-10 border-b border-t border-gray-200 py-2 md:px-12">
        <LocaleLink :to="`/pathway/edit/${generateUUID()}`"
            class="flex items-center space-x-2 rounded-lg hover:bg-gray-50 pr-1">
            <div class="bg-kashmir-500 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg">
                <PhPath class="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <h3 class="text-sm font-bold text-gray-900">
                {{ t("pathway.create") }}
            </h3>
        </LocaleLink>
        <div @click.prevent="fileClickHandler" @dragover="handleDragOver" @drop="handleDrop"
            class="flex justify-center rounded-lg border border-dashed border-gray-900/25 px-10 py-4 hover:bg-gray-50">
            <div class="flex items-center space-x-2 rounded-lg pr-1">
                <div class="bg-kashmir-500 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg">
                    <svg v-if="pathwayStore.savingDraft" aria-hidden="true"
                        class="h-4 w-4 text-kashmir-200 animate-spin fill-white" viewBox="0 0 100 101"
                        fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                            fill="currentColor" />
                        <path
                            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                            fill="currentFill" />
                    </svg>
                    <PhUploadSimple v-else class="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                <div class="flex text-sm font-bold text-gray-900">
                    <label v-if="!pathwayStore.savingDraft" for="file-upload"
                        class="relative cursor-pointer rounded-md bg-white font-bold text-kashmir-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-kashmir-900 focus-within:ring-offset-2 hover:text-kashmir-600">
                        <span>{{ t("form.upload.upload") }}</span>
                        <input id="file-upload" name="file-upload" type="file" class="sr-only" />
                    </label>
                    <p v-if="dragndrop && !pathwayStore.savingDraft" class="pl-1">{{ t("form.upload.drag") }}</p>
                    <p v-if="pathwayStore.savingDraft" class="pl-1">{{ t("pathway.journey.saving") }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { fileOpen } from "browser-fs-access"
import { PhUploadSimple, PhPath } from "@phosphor-icons/vue"
import { useToastStore, usePathwayStore } from "@/stores"
import { IKeyable } from "@/interfaces"
import { generateUUID } from "@/utilities"

const { t } = useI18n()
const toast = useToastStore()
const pathwayStore = usePathwayStore()
const importer: IKeyable = {
    mimeTypes: ["application/json"],
    extensions: [".json", ".pathway"],
    multiple: false
}
const dragndrop = ref(false)
const emit = defineEmits<{ setImport: [response: any] }>()

onMounted(async () => {
    dragndrop.value = determineDragAndDropCapable()
})

// UTILITIES
async function fileClickHandler() {
    try {
        let response: any[] | any = await fileOpen({
            mimeTypes: importer.mimeTypes,
            extensions: importer.extensions,
            multiple: importer.multiple,
        })
        response = await getJSONfromBlob(response)
        emit("setImport", response)
    } catch (error: any) {
        if (error.name !== "AbortError") {
            toast.addNotice({
                title: "Import error",
                content: `Error: ${error}`,
                icon: "error"
            })
        }
    }
}

async function handleDrop(event: DragEvent) {
    event.stopPropagation()
    event.preventDefault()
    try {
        if (event.dataTransfer && event.dataTransfer.files.length) {
            let response: any[] = []
            for (const blob of Array.from(event.dataTransfer.files)) {
                if (!importer.mimeTypes.includes(blob.type))
                    throw new Error("Not an allowed mimetype.")
                response = await getJSONfromBlob(blob)
                emit("setImport", response)
            }
        }
    } catch (error: any) {
        if (error.name !== "AbortError") {
            toast.addNotice({
                title: "Import error",
                content: `Error: ${error}`,
                icon: "error"
            })
        }
    }
}

function handleDragOver(event: DragEvent) {
    event.preventDefault()
}

async function getJSONfromBlob(payload: any): Promise<any> {
    let response = await payload.text()
    return JSON.parse(response)
}

function determineDragAndDropCapable() {
    // Complete guide to drag and drop files
    // https://serversideup.net/drag-and-drop-file-uploads-with-vuejs-and-axios/
    const div = document.createElement("div")
    return (
        ("draggable" in div || ("ondragstart" in div && "ondrop" in div)) &&
        "FormData" in window &&
        "FileReader" in window
    )
}
</script>