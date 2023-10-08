<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <PathwayEditHeadingPanel title="Testing" approach="Create" @set-edit-request="watchHeadingRequest" />
        <PathwayEditMetadataCard />
        <ul role="list">
            <li v-for="(theme, thIdx) in draft.themes" :key="`theme-${theme.id}`">
                <div class="flex justify-between -mb-2">
                    <div class="block text-xs font-medium leading-8 text-white bg-kashmir-500 mx-3 px-4 rounded-t-lg">
                        {{ t("theme.name") }}: {{ thIdx + 1 }} of {{ draft.themes.length }}
                    </div>
                    <div class="flex flex-inline items-center space-x-2 mb-1">
                        <div class="rounded-full bg-kashmir-500 p-1">
                            <PhPlus class="h-4 w-4 text-white" aria-hidden="true" />
                        </div>
                        <button type="button" @click.prevent="addTheme(theme.id)"
                            class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-kashmir-900 ring-1 ring-inset ring-kashmir-300 hover:bg-kashmir-50">
                            <PhTagSimple class="md:-ml-0.5 h-4 w-4 text-kashmir-400" aria-hidden="true" />
                            <span class="hidden md:block">{{ t("theme.name") }}</span>
                        </button>
                        <button type="button" @click.prevent="addNode(theme.id)"
                            class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-kashmir-900 ring-1 ring-inset ring-kashmir-300 hover:bg-kashmir-50">
                            <PhLineSegments class="md:-ml-0.5 h-4 w-4 text-kashmir-400" aria-hidden="true" />
                            <span class="hidden md:block">{{ t("node.name") }}</span>
                        </button>
                    </div>
                </div>
                <div :id="`${theme.id}`" draggable="true" @dragstart="handleDragStart" @dragenter="handleDragEnter"
                    @dragover="handleDragOver" @dragleave="handleDragLeave" @drop="handleDrop" @dragend="handleDragEnd"
                    class="bg-gray-50 sm:rounded-lg my-2 border-t-2 border-kashmir-500">
                    <PathwayEditThemeCard :initial-draft="theme" @set-draft="watchThemeRequest"
                        @remove-draft="removeTheme" />
                </div>
                <ul role="list">
                    <li v-for="node in theme.nodes" :key="`node-${node.id}`">
                        <div :id="`${theme.id}|${node.id}`" draggable="true" @dragstart="handleDragStart"
                            @dragenter="handleDragEnter" @dragover="handleDragOver" @dragleave="handleDragLeave"
                            @drop="handleDrop" @dragend="handleDragEnd" class="bg-gray-50 sm:rounded-lg my-2">
                            <PathwayEditNodeCard :initial-draft="node" @set-draft="watchNodeRequest" />
                        </div>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { PhPlus, PhTagSimple, PhLineSegments } from "@phosphor-icons/vue"
import { useSettingStore } from "@/stores"
import { IPathway, IKeyable, ITheme, INode } from "@/interfaces"
import { usePathwayStore } from "@/stores"
import { generateUUID } from "@/utilities"

const { t } = useI18n()
const route = useRoute()
const appSettings = useSettingStore()
const pathwayStore = usePathwayStore()
const draftPathway = ref({} as IPathway)
const draft = ref({} as IKeyable)
const dragThemeID = ref("" as string)
const dragNodeID = ref("" as string)
const isNew = ref(false)

// SETUP
onMounted(async () => {
    appSettings.setPageName("nav.pathways")
    const uuid = "0b4bd019-f5de-41b1-a3cc-a6c502c262a3"
    await pathwayStore.getTerm(uuid as string)
    if (!pathwayStore.term || Object.keys(pathwayStore.term).length === 0) {
        // The pathway doesn't exist, so create a draft ...
        isNew.value = true
        console.log("Creating a new pathway")
    }
    // if (route.params.id !== "create") {
    //     await pathwayStore.getTerm(route.params.id as string)
    //     if (!pathwayStore.term || Object.keys(pathwayStore.term).length === 0)
    //         throw createError({ statusCode: 404, statusMessage: "Page Not Found", fatal: true })
    // }

    draft.value = {
        id: generateUUID(),
        themes: [
            {
                id: generateUUID(),
                order: 0,
                nodes: [
                    {
                        id: generateUUID(),
                        order: 0,
                    }
                ]
            }
        ]
    }
})

// WATCHERS
async function watchHeadingRequest(request: string) {
    console.log("watchHeadingRequest", request)
    switch (request) {
        case "save":
            break
        case "cancel":
            break
        default:
            watchLocaleSelect(request)
            break
    }
}

async function watchMetadataRequest(request: IPathway) {

}

async function watchThemeRequest(request: ITheme) {
    console.log("watchThemeRequest", request)
    updateTheme(request)
}

async function watchNodeRequest(request: INode) {
    console.log("watchNodeRequest", request)
    updateNode(request)
}

async function watchLocaleSelect(select: string) {
    console.log("Language change", select)
    draft.value.language = select
    pathwayStore.setLanguageDraft(select)
}

// THEMES
function getThemeIndex(themeID: string) {
    return draft.value.themes.findIndex(
        (theme: ITheme) => theme.id === themeID
    )
}

function getTheme(themeID: string) {
    return draft.value.themes.find(
        (theme: ITheme) => theme.id === themeID
    )
}

function reorderThemes(frThemeID: string, toThemeID: string) {
    // Reorder themes
    const frIdx = getThemeIndex(frThemeID)
    const toIdx = getThemeIndex(toThemeID)
    // Because TypeScript, in its infinite wisdom, has no concept of `-1`
    const dragged = { ...draft.value.themes.slice(frIdx)[0] }
    draft.value.themes.splice(frIdx, 1)
    draft.value.themes.splice(toIdx, 0, dragged)
}

function moveNodeBetweenThemes(frThemeID: string, toThemeID: string, nodeID: string) {
    const frTheme = getTheme(frThemeID)
    const frIdx = getNodeIndex(frTheme, nodeID)
    const toTheme = getTheme(toThemeID)
    const dragged = { ...frTheme.nodes.slice(frIdx)[0] }
    // make sure this is reassigned
    dragged.theme_id = toTheme.id
    frTheme.nodes.splice(frIdx, 1)
    toTheme.nodes.push(dragged)
}

function addTheme(requestThemeID: string) {
    const newTheme = {
        id: generateUUID(),
        nodes: [
            {
                id: generateUUID()
            }
        ]
    }
    draft.value.themes.push(newTheme)
    reorderThemes(newTheme.id, requestThemeID)
}

function updateTheme(update: ITheme) {
    const updateIdx = getThemeIndex(update.id as string)
    update.nodes = draft.value.themes[updateIdx].nodes
    draft.value.themes[updateIdx] = update
}

function removeTheme(themeID: string) {
    const themeIdx = getThemeIndex(themeID)
    draft.value.themes.splice(themeIdx, 1)
}

// NODES
function getNodeIndex(theme: ITheme, nodeID: string) {
    return theme.nodes!.findIndex(
        (node: INode) => node.id === nodeID
    )
}

function getNode(theme: ITheme, nodeID: string) {
    return theme.nodes!.find(
        (node: INode) => node.id === nodeID
    )
}

function reorderNodes(theme: ITheme, frNodeID: string, toNodeID: string) {
    // Reorder themes
    const frIdx = getNodeIndex(theme, frNodeID)
    const toIdx = getNodeIndex(theme, toNodeID)
    const dragged = { ...theme.nodes!.slice(frIdx)[0] }
    theme.nodes!.splice(frIdx, 1)
    theme.nodes!.splice(toIdx, 0, dragged)
}

function addNode(themeID: string, requestNodeID?: string) {
    const theme = getTheme(themeID)
    const newNode = {
        id: generateUUID(),
        theme_id: theme.id
    }
    theme.nodes.push(newNode)
    if (requestNodeID) reorderNodes(theme, newNode.id, requestNodeID)
}

function updateNode(update: INode) {
    const themeIdx = getThemeIndex(update.theme_id as string)
    const theme = getTheme(update.theme_id as string)
    const updateIdx = getNodeIndex(theme, update.id as string)
    draft.value.themes[themeIdx].nodes[updateIdx] = update
}

function removeNode(themeID: string, nodeID: string) {
    const theme = getTheme(themeID)
    const nodeIdx = getNodeIndex(theme, nodeID)
    theme.nodes!.splice(nodeIdx, 1)
}

// DRAG N DROP
// https://web.dev/drag-and-drop/
function handleDragStart(e: any) {
    e.currentTarget.className = e.currentTarget.className.replace(
        "bg-gray-50",
        "bg-cerise-100"
    )
    const dragIDs = e.currentTarget.id.split("|")
    dragThemeID.value = dragIDs[0]
    dragNodeID.value = ""
    if (dragIDs.length === 2) {
        dragNodeID.value = dragIDs[1]
    }
    e.dataTransfer.effectAllowed = "move"
    e.dataTransfer.setData("id", e.currentTarget.id)
}

function handleDragEnter(e: any) {
    if (e.target.id !== e.currentTarget.id) return false
    e.currentTarget.className = e.currentTarget.className.replace(
        "bg-gray-50",
        "bg-cerise-100"
    )
}

function handleDragOver(e: any) {
    if (e.preventDefault) {
        e.preventDefault() // Necessary. Allows us to drop.
    }
    if (e.target.id !== e.currentTarget.id) return false
    e.dataTransfer.dropEffect = "move"
    return false
}

function handleDragLeave(e: any) {
    e.stopPropagation()
    if (e.target.id !== e.currentTarget.id) return false
    e.currentTarget.className = e.currentTarget.className.replace(
        "bg-cerise-100",
        "bg-gray-50"
    )
}

function handleDrop(e: any) {
    e.stopPropagation()
    e.preventDefault()
    const dropID = e.currentTarget.id.split("|")
    const dropThemeID = dropID[0]
    let dropNodeID = ""
    if (dropID.length === 2) {
        dropNodeID = dropID[1]
    }
    // Drag - Theme | Node && Drop - Theme | Node
    // Theme to Theme, reorder | Theme to Node, ignore
    // Node to Theme, push / remove | Node to Node, reorder (with variations)
    if (
        (dragThemeID.value !== dropThemeID)
        && (dragNodeID.value === "")
    ) {
        // Reorder themes
        reorderThemes(dragThemeID.value, dropThemeID)
    } else if (
        (dragThemeID.value !== dropThemeID)
        && (dragNodeID.value !== "")
        && (dropNodeID === "")
    ) {
        moveNodeBetweenThemes(dragThemeID.value, dropThemeID, dragNodeID.value)
    } else if (
        (dragThemeID.value === dropThemeID)
        && (dragNodeID.value !== dropNodeID)
    ) {
        const dragTheme = getTheme(dragThemeID.value)
        reorderNodes(dragTheme, dragNodeID.value, dropNodeID)
    }
    e.currentTarget.className = e.currentTarget.className.replace(
        "bg-cerise-100",
        "bg-gray-50"
    )
    return false
}

function handleDragEnd(e: any) {
    if (e.target.id !== e.currentTarget.id) return false
    e.currentTarget.className = e.currentTarget.className.replace(
        "bg-cerise-100",
        "bg-gray-50"
    )
}
</script>