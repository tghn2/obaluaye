<template>
    <div>
        <p class="text-sm font-medium text-gray-900 mb-2">{{ t("form.types.selectmany") }}</p>
        <div v-for="term in props.form.terms" class="group flex items-center gap-x-3 text-sm leading-6 sm:px-1">
            <PhSquare class="text-gray-400 h-4 w-4 shrink-0" aria-hidden="true" />
            <span class="text-sm text-gray-900">{{ term.value }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhSquare } from "@phosphor-icons/vue"
import { IForm } from "@/interfaces"

const { t } = useI18n()

const props = defineProps<{
    form: IForm,
}>()
</script>