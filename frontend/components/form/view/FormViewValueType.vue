<template>
    <div>
        <p class="text-sm font-medium text-gray-900 mb-2">{{ t("form.types.value") }}</p>
        <div class="group flex items-center gap-x-3 text-sm leading-6 sm:px-1">
            <PhCircle class="text-gray-400 h-4 w-4 shrink-0" aria-hidden="true" />
            <span class="text-sm text-gray-900">{{ t("form.valueText") }} {{ t(inputType[props.form.constraints.dtype])
            }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhCircle } from "@phosphor-icons/vue"
import { IForm, IKeyable } from "@/interfaces"

const { t } = useI18n()
const inputType: IKeyable = {
    DATE: "form.values.date",
    DATETIME: "form.values.datetime",
    YEAR: "form.values.year",
    NUMBER: "form.values.number",
    INTEGER: "form.values.integer",
    BOOLEAN: "form.values.boolean",
    ARRAY: "form.values.array",
    STRING: "form.values.string",
}
const props = defineProps<{
    form: IForm,
}>()
</script>