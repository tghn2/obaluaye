<template>
    <div>
        <p class="text-sm font-medium text-gray-900 mb-2">{{ t("form.types.selectbranch") }}</p>
        <div v-for="term in props.form.terms" class="group flex items-center gap-x-3 text-sm leading-6 sm:px-1">
            <PhCircle class="text-gray-400 h-4 w-4 shrink-0" aria-hidden="true" />
            <span class="text-sm text-gray-900">{{ term.value }}</span>
            <span aria-hidden="true">→</span>
            <span class="text-sm text-gray-900">
                <!-- @vue-ignore -->
                <!-- @vue-expect-error -->
                {{ pathwayStore.term.themes.find((b: IKeyable) => b.id === term.branch).title }}
            </span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhCircle } from "@phosphor-icons/vue"
import { usePathwayStore } from "@/stores"
import { IForm } from "@/interfaces"

const { t } = useI18n()
const pathwayStore = usePathwayStore()

const props = defineProps<{
    form: IForm,
}>()
</script>