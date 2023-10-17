<template>
    <fieldset>
        <div v-if="!draft || !draft.answer || Object.keys(draft.answer).length === 0" @click.prevent="fileClickHandler"
            @dragover="handleDragOver" @drop="handleDrop"
            class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
            <div class="text-center">
                <PhUploadSimple class="mx-auto h-12 w-12 text-gray-300" aria-hidden="true" />
                <div class="mt-4 flex text-sm leading-6 text-gray-600">
                    <label for="file-upload"
                        class="relative cursor-pointer rounded-md bg-white font-semibold text-ochre-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-ochre-600 focus-within:ring-offset-2 hover:text-ochre-500">
                        <span>{{ t("form.upload.upload") }}</span>
                        <input id="file-upload" name="file-upload" type="file" class="sr-only" />
                    </label>
                    <p v-if="dragndrop" class="pl-1">{{ t("form.upload.drag") }}</p>
                    <p class="pl-1">{{ t("form.upload.afile") }}</p>
                </div>
            </div>
        </div>
        <div v-else class="flex items-center justify-between">
            <span v-if="draft && draft.answer && !Array.isArray(draft.answer) && Object.keys(draft.answer).length"
                class="text-sm text-gray-700">
                {{ draft.answer.value }}
            </span>
            <button type="button" @click="removeUpload"
                class="relative items-center rounded-full p-1 text-cerise-700 hover:bg-cerise-50">
                <PhX class="h-5 w-5" aria-hidden="true" />
            </button>
        </div>
    </fieldset>
</template>

<script setup lang="ts">
import { fileOpen } from "browser-fs-access"
import { PhUploadSimple, PhX } from "@phosphor-icons/vue"
import { INode, IAnswer, IAnswerResponse } from "@/interfaces"
import { useTokenStore, useToastStore, useJourneyStore } from "@/stores"
import { apiResponse } from "@/api"

const { t } = useI18n()
const tokenStore = useTokenStore()
const toastStore = useToastStore()
const journeyStore = useJourneyStore()
const draft = ref({} as IAnswerResponse)
const validated = ref(false)
const dragndrop = ref(false)

const props = defineProps<{
    node: INode,
}>()
const emit = defineEmits<{ setResponse: [draft: IAnswerResponse] }>()

// WATCHERS
watch(
    () => draft.value, () => {
        let response = { ...draft.value }
        response.validated = validate()
        emit("setResponse", response)
    },
    { deep: true }
)

// VALIDATORS
function validate(): boolean {
    return false
}

// UPLOAD UTILITIES
async function fileClickHandler() {
    let answer = {} as IAnswer
    try {
        let response: File = await fileOpen()
        if (response) answer = {
            id: journeyStore.sourceKey,
            value: response.name,
            dtype: response.type
        }
        // upload the thing
        await uploadSource(response)
        draft.value.answer = { ...answer }
    } catch (error: any) {
        if (error.name !== "AbortError") {
            toastStore.addNotice({
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
            let answer = {} as IAnswer
            let response: File
            for (const blob of Array.from(event.dataTransfer.files)) {
                // Only going to take one ... up to the user to realise this.
                response = blob
                answer = {
                    id: journeyStore.sourceKey,
                    value: blob.name,
                    dtype: blob.type
                }
                // upload the thing
                await uploadSource(response)
                break
            }
            draft.value.answer = { ...answer }
        }
    } catch (error: any) {
        if (error.name !== "AbortError") {
            toastStore.addNotice({
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

// MANAGE UPLOAD
async function uploadSource(source: File) {
    let formData: FormData = new FormData()
    formData.append("files", source, source.name)
    await tokenStore.refreshTokens()
    await apiResponse.createUploadTerm(
        tokenStore.token,
        formData,
        props.node.id as string,
        journeyStore.sourceKey
    )
}

async function removeSource() {
    // https://stackoverflow.com/a/71942120/295606
    if (draft.value.answer && !Array.isArray(draft.value.answer) && Object.keys(draft.value.answer).length) {
        await tokenStore.refreshTokens()
        await apiResponse.removeUploadTerm(
            tokenStore.token,
            props.node.id as string,
            draft.value.answer.id as string
        )
    }
}

// function returnSource(response: any) {
//     if (draft.value.answer && !Array.isArray(draft.value.answer) && Object.keys(draft.value.answer).length) {
//         // https://stackoverflow.com/a/18197341/295606
//         const mimeType = draft.value.answer.dtype
//         const a = document.createElement("a")
//         const data = `data:${mimeType},${encodeURIComponent(response)}`
//         a.href = data
//         a.download = draft.value.answer.value
//         a.type = mimeType
//         a.style.display = "none"
//         document.body.appendChild(a)
//         a.click()
//         document.body.removeChild(a)
//     }
// }

// async function getSource() {
//     if (draft.value.answer && !Array.isArray(draft.value.answer) && Object.keys(draft.value.answer).length) {
//         try {
//             const { data: response } = await apiResponse.getUploadTerm(props.node.id as string, draft.value.answer.id as string)
//             if (response.value) {
//                 return returnSource(response.value)
//             }
//         } catch (error) {
//             toastStore.addNotice({
//                 title: "Download error",
//                 content: error as string,
//                 icon: "error"
//             })
//         }
//     }
// }

// SETTERS
function resetDraft() {
    // Setup AnswerResponse
    let initialDraft = {} as IAnswerResponse
    if (props.node.response && Object.keys(props.node.response).length && props.node.response.answer) {
        initialDraft = {
            answer: { ...props.node.response.answer }
        }
    }
    if (Object.keys(initialDraft).length === 0) {
        initialDraft = {
            answer: {} as IAnswer,
        }
    }
    draft.value = { ...initialDraft }
    validated.value = validate()
}

async function removeUpload() {
    const initialDraft: IAnswerResponse = {
        answer: {} as IAnswer
    }
    // remove uplodate    
    await removeSource()
    draft.value = { ...initialDraft }
    validated.value = validate()
}

onMounted(async () => {
    dragndrop.value = determineDragAndDropCapable()
    resetDraft()
})
</script>