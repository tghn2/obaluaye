<template>
    <fieldset class="mt-2">
        <div class="flex space-x-4 items-center text-sm text-gray-900">
            <span v-if="dtype === 'DATE'">{{ readableDate(term, true, props.node.language) }}</span>
            <span v-else>{{ term }}</span>
        </div>
        <p v-if="props.node.form && props.node.form.constraints" class="mt-2 text-sm leading-6 text-gray-500">
            <span v-if="props.node.form.constraints.minimum">{{ t("form.constraints.minimum") }}: {{
                props.node.form.constraints.minimum }}</span>
            <span v-if="props.node.form.constraints.limit && props.node.form.constraints.minimum">&nbsp;&&nbsp;</span>
            <span v-if="props.node.form.constraints.maximum">{{ t("form.constraints.maximum") }}: {{
                props.node.form.constraints.maximum }}</span>
        </p>
    </fieldset>
</template>

<script setup lang="ts">
import { INode } from "@/interfaces"
import { readableDate } from "@/utilities"

const { t } = useI18n()
const dtype = ref("NUMBER" as IValueType)
const inputTypes: IValueType[] = ["DATE", "DATETIME"]
const term = ref("")

const props = defineProps<{
    node: INode,
}>()

// SETTERS
function setReview() {
    if (
        props.node.response
        && Object.keys(props.node.response).length
        && props.node.response.answer
        && !Array.isArray(props.node.response.answer)
    ) {
        term.value = props.node.response.answer.value
    }
    if (
        props.node.form
        && props.node.form.constraints
        && props.node.form.constraints.dtype
        && inputTypes.includes(props.node.form.constraints.dtype)
    ) {
        dtype.value = "DATE"
    }
}
onMounted(async () => {
    setReview()
})
</script>