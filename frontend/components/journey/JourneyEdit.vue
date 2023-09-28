<template>
    <div class="mx-auto min-w-full">
        <JourneyHeadingEditPanel title="Testing" :approach="props.approach" @set-edit-request="watchEditHeadingRequest" />
        <JourneyDisclosurePanel />
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    approach: string
}>()

async function watchEditHeadingRequest(request: string) {
    console.log("watchEditHeadingRequest", request)
    switch (request) {
        case "reset":
            break
        case "save":
            break
        case "cancel":
            break
        default:
            watchLocaleSelect(request)
            break
    }
}

async function watchLocaleSelect(select: string) {
    console.log("Language change", select)
}
</script>