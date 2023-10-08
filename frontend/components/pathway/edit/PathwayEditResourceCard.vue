<template>
    <div class="max-w-3xl">
        <div class="block text-sm font-semibold leading-6 text-gray-900">
            {{ t("resource.name") }}
        </div>
        <div class="mt-2">
            <div class="mt-2">
                <table class="min-w-full">
                    <tbody>
                        <tr v-for="(resource, resourceIdx) in drafts" :key="`resource-${resource.id}`"
                            class="relative w-full ">
                            <td class="px-3 text-sm text-gray-700">
                                {{ resource.title }}
                            </td>
                            <td class="relative pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                                <div class="flex flex-inline items-center space-x-2 justify-end">
                                    <ResourceEditModal :initial-draft="resource" @set-draft="watchResourceUpdate" />
                                    <button type="button" @click="removeResource(resourceIdx)"
                                        class="relative items-center rounded-full p-1 text-cerise-700 hover:bg-cerise-50">
                                        <PhX class="h-5 w-5" aria-hidden="true" />
                                    </button>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class="px-3 text-sm text-gray-700 italic">
                                {{ t("resource.new") }}
                            </td>
                            <td class="relative py-2 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                                <ResourceEditModal :initial-draft="{} as IResource" @set-draft="watchResourceUpdate" />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhX } from "@phosphor-icons/vue"
import { IResource } from "@/interfaces"
import { useTokenStore } from "@/stores"
import { apiResource } from "@/api"

const { t } = useI18n()
const drafts = ref([] as IResource[])

const props = defineProps<{
    initialDrafts?: IResource[],
}>()
const emit = defineEmits<{
    setDrafts: [drafts: IResource[]],
}>()

// WATCHERS
function watchResourceUpdate(update: IResource) {
    updateResource(update)
    emit("setDrafts", drafts.value)
}

// UPDATERS
function getResourceIndex(resourceID: string) {
    return drafts.value.findIndex(
        (resource: IResource) => resource.id === resourceID
    )
}

function updateResource(update: IResource) {
    const updateIdx = getResourceIndex(update.id as string)
    if (updateIdx < 0) drafts.value.push(update)
    else drafts.value![updateIdx] = update
}

async function removeResource(resourceIdx: number) {
    if (drafts.value && drafts.value.length) {
        const resourceID = drafts.value[resourceIdx].id
        drafts.value.splice(resourceIdx, 1)
        // Delete it directly here first
        const tokenStore = useTokenStore()
        try {
            await apiResource.removeTerm(tokenStore.token, resourceID as string)
        } catch (error) { }
    }
}

// SETTERS
onMounted(async () => {
    reset()
})

function reset() {
    if (props.initialDrafts && props.initialDrafts.length) drafts.value = props.initialDrafts
}

onMounted(async () => {
    reset()
})
</script>