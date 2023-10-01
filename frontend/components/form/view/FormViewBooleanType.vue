<template>
    <div>
        <p class="text-sm font-medium text-gray-900 mb-2">{{ t("form.types.boolean") }}</p>
        <div v-for="term in ['form.booleanTrue', 'form.booleanFalse']" class="inline-flex">
            <div class="group flex items-center gap-x-1 text-sm leading-6 px-2">
                <PhCircle class="text-gray-400 h-4 w-4 shrink-0" aria-hidden="true" />
                <span class="text-sm text-gray-900">{{ t(term) }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhCircle } from "@phosphor-icons/vue"
import { IForm } from "@/interfaces"

const { t } = useI18n()

const props = defineProps<{
    form: IForm,
}>()
</script>