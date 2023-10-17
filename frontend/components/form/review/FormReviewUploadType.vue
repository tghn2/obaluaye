<template>
    <fieldset>
        <button @click="getSource"
            class="inline-flex items-center group test-sm font-medium text-kashmir-800 hover:text-kashmir-600">
            <PhLinkSimple class="h-4 w-4 mr-1" aria-hidden="true" />
            <span>{{ term.value }}</span>
        </button>
    </fieldset>
</template>

<script setup lang="ts">
import { PhLinkSimple } from "@phosphor-icons/vue"
import { INode, IKeyable } from "@/interfaces"
import { useToastStore } from "@/stores"
import { apiResponse } from "@/api"

const term = ref({} as IKeyable)
const toastStore = useToastStore()

const props = defineProps<{
    node: INode,
}>()

// MANAGE UPLOAD
function getEncodedResponse(mimeType: string, response: any) {
    switch (mimeType) {
        case "application/json":
            return `data:${mimeType},${encodeURIComponent(JSON.stringify(response))}`
        case "text/csv":
            return `data:${mimeType},${encodeURIComponent(response)}`
        default:
            // it's a blob ...
            return URL.createObjectURL(response)
    }
}

function returnSource(response: any) {
    if (Object.keys(term.value).length) {
        // https://stackoverflow.com/a/18197341/295606
        const mimeType = term.value.dtype
        const a = document.createElement("a")
        const data = getEncodedResponse(mimeType, response)
        a.href = data
        a.download = term.value.value
        a.type = mimeType
        a.style.display = "none"
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
    }
}

async function getSource() {
    if (Object.keys(term.value).length) {
        try {
            const { data: response } = await apiResponse.getUploadTerm(props.node.id as string, term.value.id as string)
            if (response.value) {
                return returnSource(response.value)
            }
        } catch (error) {
            toastStore.addNotice({
                title: "Download error",
                content: error as string,
                icon: "error"
            })
        }
    }
}

// SETTERS
function setReview() {
    if (props.node.response && Object.keys(props.node.response).length && props.node.response.answer) {
        term.value = { ...props.node.response.answer }
    }
}

onMounted(async () => {
    setReview()
})
</script>