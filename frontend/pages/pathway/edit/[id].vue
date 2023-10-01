<template>
    <div class="px-2 py-10 lg:px-4 lg:py-6 max-w-3xl mx-auto">
        <div v-if="appSettings.current.pageState === 'loading'">
            <LoadingCardSkeleton />
        </div>
        <div v-if="appSettings.current.pageState === 'done'">
            <PathwayEditHeadingPanel :title="pathTitle" @set-edit-request="watchHeadingRequest" />
            <div class="flex justify-between -mb-2 mt-2">
                <div class="block text-xs font-medium leading-6 text-white bg-spring-700 mx-3 px-3 pt-0.5 rounded-t-lg">
                    {{ t("pathway.metadata") }}
                </div>
                <div class="flex flex-inline items-center space-x-2 mb-1">
                    <div class="rounded-full bg-spring-400 p-1">
                        <PhPlus class="h-4 w-4 text-white" aria-hidden="true" />
                    </div>
                    <button type="button" @click.prevent="addTheme()"
                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-spring-900 ring-1 ring-inset ring-spring-300 hover:bg-spring-50">
                        <PhTagSimple class="md:-ml-0.5 h-4 w-4 text-spring-400" aria-hidden="true" />
                        <span class="hidden md:block">{{ t("theme.name") }}</span>
                    </button>
                    <button type="button"
                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-spring-900 ring-1 ring-inset ring-spring-300 hover:bg-spring-50">
                        <PhBookmarkSimple class="md:-ml-0.5 h-4 w-4 text-spring-400" aria-hidden="true" />
                        <span class="hidden md:block">{{ t("resource.name") }}</span>
                    </button>
                </div>
            </div>
            <div class="rounded-lg my-2 border-t-2 border-spring-700">
                <PathwayEditMetadataCard :initial-draft="draft" @set-draft="watchMetadataRequest" />
            </div>
            <ul role="list">
                <li v-for="(theme, thIdx) in draft.themes" :key="`theme-${theme.id}`">
                    <div class="flex justify-between -mb-2">
                        <div
                            class="block text-xs font-medium leading-6 text-white bg-spring-500 mx-3 px-3 pt-0.5 rounded-t-lg">
                            {{ t("theme.name") }}: {{ thIdx + 1 }} of {{ draft.themes!.length }}
                        </div>
                        <div class="flex flex-inline items-center space-x-2 mb-1">
                            <div class="rounded-full bg-rose-400 p-1">
                                <PhMinus class="h-4 w-4 text-white" aria-hidden="true" />
                            </div>
                            <button type="button" @click.prevent="removeTheme(theme.id as string)"
                                class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-rose-900 ring-1 ring-inset ring-rose-300 hover:bg-rose-50">
                                <PhTrashSimple class="md:-ml-0.5 h-4 w-4 text-rose-400" aria-hidden="true" />
                                <span class="hidden md:block">{{ t("header.delete") }}</span>
                            </button>
                            <div class="rounded-full bg-spring-500 p-1">
                                <PhPlus class="h-4 w-4 text-white" aria-hidden="true" />
                            </div>
                            <button type="button" @click.prevent="addTheme(theme.id as string)"
                                class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-spring-900 ring-1 ring-inset ring-spring-300 hover:bg-spring-50">
                                <PhTagSimple class="md:-ml-0.5 h-4 w-4 text-spring-400" aria-hidden="true" />
                                <span class="hidden md:block">{{ t("theme.name") }}</span>
                            </button>
                            <button type="button" @click.prevent="addNode(theme.id as string)"
                                class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-spring-900 ring-1 ring-inset ring-spring-300 hover:bg-spring-50">
                                <PhLineSegments class="md:-ml-0.5 h-4 w-4 text-spring-400" aria-hidden="true" />
                                <span class="hidden md:block">{{ t("node.name") }}</span>
                            </button>
                            <button type="button"
                                class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-spring-900 ring-1 ring-inset ring-spring-300 hover:bg-spring-50">
                                <PhBookmarkSimple class="md:-ml-0.5 h-4 w-4 text-spring-400" aria-hidden="true" />
                                <span class="hidden md:block">{{ t("resource.name") }}</span>
                            </button>
                        </div>
                    </div>
                    <div :id="`${theme.id}`" :draggable="theme.id !== pathwayStore.activeDraft" @dragstart="handleDragStart"
                        @dragenter="handleDragEnter" @dragover="handleDragOver" @dragleave="handleDragLeave"
                        @drop="handleDrop" @dragend="handleDragEnd"
                        class="bg-gray-50 rounded-lg my-2 border-t-2 border-spring-500">
                        <PathwayEditThemeCard :initial-draft="theme" @set-draft="watchThemeRequest" />
                    </div>
                    <ul role="list">
                        <li v-for="(node, ndIdx) in theme.nodes" :key="`node-${node.id}`">
                            <div class="flex justify-between -mb-2">
                                <div
                                    class="block text-xs font-medium leading-6 text-white bg-spring-300 mx-3 px-3 pt-0.5 rounded-t-lg">
                                    {{ t("node.name") }}: {{ ndIdx + 1 }} of {{ theme.nodes!.length }}
                                </div>
                                <div class="flex flex-inline items-center space-x-2 mb-1">
                                    <div class="rounded-full bg-rose-300 p-1">
                                        <PhMinus class="h-4 w-4 text-white" aria-hidden="true" />
                                    </div>
                                    <button type="button" @click.prevent="removeNode(theme.id as string, node.id as string)"
                                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-rose-900 ring-1 ring-inset ring-rose-300 hover:bg-rose-50">
                                        <PhTrashSimple class="md:-ml-0.5 h-4 w-4 text-rose-400" aria-hidden="true" />
                                        <span class="hidden md:block">{{ t("header.delete") }}</span>
                                    </button>
                                    <div class="rounded-full bg-spring-300 p-1">
                                        <PhPlus class="h-4 w-4 text-white" aria-hidden="true" />
                                    </div>
                                    <button type="button" @click.prevent="addNode(theme.id as string, node.id as string)"
                                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-spring-900 ring-1 ring-inset ring-spring-300 hover:bg-spring-50">
                                        <PhLineSegments class="md:-ml-0.5 h-4 w-4 text-spring-400" aria-hidden="true" />
                                        <span class="hidden md:block">{{ t("node.name") }}</span>
                                    </button>
                                    <button type="button"
                                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-2 py-1 text-xs text-spring-900 ring-1 ring-inset ring-spring-300 hover:bg-spring-50">
                                        <PhBookmarkSimple class="md:-ml-0.5 h-4 w-4 text-spring-400" aria-hidden="true" />
                                        <span class="hidden md:block">{{ t("resource.name") }}</span>
                                    </button>
                                </div>
                            </div>
                            <div :id="`${theme.id}|${node.id}`" :draggable="node.id !== pathwayStore.activeDraft"
                                @dragstart="handleDragStart" @dragenter="handleDragEnter" @dragover="handleDragOver"
                                @dragleave="handleDragLeave" @drop="handleDrop" @dragend="handleDragEnd"
                                class="bg-gray-50 rounded-lg my-2 border-t-2 border-spring-300">
                                <PathwayEditNodeCard :initial-draft="node" @set-draft="watchNodeRequest" />
                            </div>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPlus, PhMinus, PhTagSimple, PhLineSegments, PhBookmarkSimple, PhTrashSimple } from "@phosphor-icons/vue"
import { useSettingStore, usePathwayStore } from "@/stores"
import { IPathway, IKeyable, ITheme, INode, IPathwayType } from "@/interfaces"
import { generateUUID } from "@/utilities"

definePageMeta({
    middleware: ["moderator"],
});

const { t } = useI18n()
const route = useRoute()
const appSettings = useSettingStore()
const pathwayStore = usePathwayStore()
const draft = ref({} as IPathway)
const draftStartLanguage = ref("")
const dragThemeID = ref("" as string)
const dragNodeID = ref("" as string)
const pathTitle = ref("Creating pathway")

// SETUP
onMounted(async () => {
    appSettings.setPageName("nav.pathways")
    await pathwayStore.getTerm(route.params.id as string, false)
    if (!pathwayStore.term || Object.keys(pathwayStore.term).length === 0) {
        // The pathway doesn't exist, so create a draft ...
        pathwayStore.setCreateDraft(true)
        createDraft()
    } else {
        pathwayStore.setCreateDraft(false)
        pathTitle.value = "Updating pathway"
        resetDraft()
    }
    draftStartLanguage.value = draft.value.language as string
    pathwayStore.settings.setPageState("done")
})

function createDraft() {
    pathwayStore.setLanguageDraft(pathwayStore.settings.locale)
    const themeID = generateUUID()
    draft.value = {
        id: route.params.id as string,
        isPrivate: true,
        isProtected: true,
        pathType: "RESEARCH",
        language: pathwayStore.languageDraft,
        themes: [
            {
                id: themeID,
                language: pathwayStore.languageDraft,
                nodes: [
                    {
                        id: generateUUID(),
                        language: pathwayStore.languageDraft,
                        formType: "SELECTONE",
                        form: {},
                        resources: [],
                        theme_id: themeID,
                    },
                ],
                resources: [],
                pathway_id: route.params.id as string,
            }
        ],
        resources: [],
    }
}

function resetDraft() {
    pathwayStore.setLanguageDraft(pathwayStore.term.language as string)
    draft.value = { ...pathwayStore.term }
}

// WATCHERS
async function watchHeadingRequest(request: string) {
    console.log("watchHeadingRequest", request)
    switch (request) {
        case "save":
            await pathwayStore.updateTerm(route.params.id as string, draft.value)
            break
        case "cancel":
            return await navigateTo(`/pathway/${route.params.id}`)
        default:
            watchLocaleSelect(request)
            break
    }
}

async function watchMetadataRequest(request: IPathway) {
    // console.log("watchMetadataRequest", request)
    updatePathwayMetadata(request)
}

async function watchThemeRequest(request: ITheme) {
    // console.log("watchThemeRequest", request)
    updateTheme(request)
}

async function watchNodeRequest(request: INode) {
    // console.log("watchNodeRequest", request)
    updateNode(request)
}

async function watchLocaleSelect(select: string) {
    // console.log("Language change", select)
    pathwayStore.setLanguageDraft(select)
    pathwayStore.setIsTranslatingDraft(select !== draftStartLanguage.value)
}

watch(
    () => draft.value, () => {
        if (Object.keys(draft.value).length !== 0) pathwayStore.setDraft({ ...draft.value })
    },
    { deep: true }
)

// GETTERS
function getThemeIndex(themeID: string) {
    return draft.value.themes!.findIndex(
        (theme: ITheme) => theme.id === themeID
    )
}

function getTheme(themeID: string) {
    return draft.value.themes!.find(
        (theme: ITheme) => theme.id === themeID
    )
}

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

// CREATORS UPDATERS
function updatePathwayMetadata(update: IPathway) {
    if (draft.value.themes && draft.value.themes.length) update.themes = [...draft.value.themes]
    if (draft.value.resources && draft.value.resources.length) update.resources = [...draft.value.resources]
    draft.value = { ...update }
}

function updateTheme(update: ITheme) {
    const updateIdx = getThemeIndex(update.id as string)
    update.nodes = draft.value.themes![updateIdx].nodes
    draft.value.themes![updateIdx] = update
}

function updateNode(update: INode) {
    const themeIdx = getThemeIndex(update.theme_id as string)
    const theme = getTheme(update.theme_id as string)
    const updateIdx = getNodeIndex(theme as ITheme, update.id as string)
    draft.value.themes![themeIdx].nodes![updateIdx] = update
}

function addTheme(requestThemeID?: string) {
    const themeID = generateUUID()
    const newTheme: ITheme = {
        id: themeID,
        language: draft.value.language,
        nodes: [{
            id: generateUUID(),
            language: draft.value.language,
            form: {},
            resources: [],
            theme_id: themeID,
        }],
        resources: [],
        pathway_id: route.params.id as string,
    }
    draft.value.themes!.push(newTheme)
    if (requestThemeID) reorderThemes(newTheme.id as string, requestThemeID)
}

function addNode(themeID: string, requestNodeID?: string) {
    const theme = getTheme(themeID)
    const newNode = {
        id: generateUUID(),
        language: draft.value.language,
        form: {},
        resources: [],
        theme_id: theme!.id
    }
    theme!.nodes!.push(newNode)
    if (requestNodeID) reorderNodes(theme as ITheme, newNode.id, requestNodeID)
}

// REORDER MOVERS
function reorderThemes(frThemeID: string, toThemeID: string) {
    // Reorder themes
    const frIdx = getThemeIndex(frThemeID)
    const toIdx = getThemeIndex(toThemeID)
    // Because TypeScript, in its infinite wisdom, has no concept of `-1`
    const dragged = { ...draft.value.themes!.slice(frIdx)[0] }
    draft.value.themes!.splice(frIdx, 1)
    draft.value.themes!.splice(toIdx, 0, dragged)
}

function moveNodeBetweenThemes(frThemeID: string, toThemeID: string, nodeID: string) {
    const frTheme = getTheme(frThemeID)
    const frIdx = getNodeIndex(frTheme as ITheme, nodeID)
    const toTheme = getTheme(toThemeID)
    const dragged = { ...frTheme!.nodes!.slice(frIdx)[0] }
    // make sure this is reassigned
    dragged.theme_id = toTheme!.id
    frTheme!.nodes!.splice(frIdx, 1)
    toTheme!.nodes!.push(dragged)
}

function reorderNodes(theme: ITheme, frNodeID: string, toNodeID: string) {
    // Reorder themes
    const frIdx = getNodeIndex(theme, frNodeID)
    const toIdx = getNodeIndex(theme, toNodeID)
    const dragged = { ...theme.nodes!.slice(frIdx)[0] }
    theme.nodes!.splice(frIdx, 1)
    theme.nodes!.splice(toIdx, 0, dragged)
}

// DELETERS
function removeTheme(themeID: string) {
    const themeIdx = getThemeIndex(themeID)
    draft.value.themes!.splice(themeIdx, 1)
}

function removeNode(themeID: string, nodeID: string) {
    const theme = getTheme(themeID)
    const nodeIdx = getNodeIndex(theme as ITheme, nodeID)
    theme!.nodes!.splice(nodeIdx, 1)
}

// DRAG N DROP
// https://web.dev/drag-and-drop/
function handleDragStart(e: any) {
    e.currentTarget.className = e.currentTarget.className.replace(
        "bg-gray-50",
        "bg-rose-100"
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
        "bg-rose-100"
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
        "bg-rose-100",
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
        reorderNodes(dragTheme as ITheme, dragNodeID.value, dropNodeID)
    }
    e.currentTarget.className = e.currentTarget.className.replace(
        "bg-rose-100",
        "bg-gray-50"
    )
    return false
}

function handleDragEnd(e: any) {
    if (e.target.id !== e.currentTarget.id) return false
    e.currentTarget.className = e.currentTarget.className.replace(
        "bg-rose-100",
        "bg-gray-50"
    )
}

onBeforeRouteLeave((to, from, next) => {
    if (Object.keys(draft.value).length !== 0) pathwayStore.setDraft({ ...draft.value })
    next()
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