<template>
    <SwitchGroup as="div" class="flex flex-wrap justify-center mx-3 my-2">
        <SwitchLabel as="span" class="text-sm">
            <span v-if="!pathwayStore.term.isPrivate" class="block text-xs">{{ t("pathway.unpublish") }}</span>
            <span v-else class="block text-xs">{{ t("pathway.publish") }}</span>
        </SwitchLabel>
        <Switch v-model="checkState" @click="submit"
            class="group relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer items-center justify-center rounded-full focus:outline-none">
            <span class="sr-only">{{ t("filter.featured") }}</span>
            <span aria-hidden="true" class="pointer-events-none absolute h-full w-full rounded-md bg-white" />
            <span aria-hidden="true"
                :class="[checkState ? 'bg-kashmir-600' : 'bg-gray-200', 'pointer-events-none absolute mx-auto h-3 w-8 rounded-full transition-colors duration-200 ease-in-out']" />
            <span aria-hidden="true"
                :class="[checkState ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none absolute left-0 inline-block h-4 w-4 transform rounded-full border border-gray-200 bg-white shadow ring-0 transition-transform duration-200 ease-in-out']" />
        </Switch>
    </SwitchGroup>
</template>

<script setup lang="ts">
import { Switch, SwitchGroup, SwitchLabel } from "@headlessui/vue"
import { usePathwayStore } from "@/stores"

const { t } = useI18n()
const route = useRoute()
const pathwayStore = usePathwayStore()
const checkState = ref(false)

async function submit() {
    await pathwayStore.toggleTerm(route.params.id as string)
    reset()
}

function reset() {
    // opposite state !isPrivate === published
    checkState.value = pathwayStore.term.isPrivate ? false : true
}

onMounted(() => {
    reset()
})
</script>