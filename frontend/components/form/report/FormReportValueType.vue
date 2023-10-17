<template>
    <fieldset class="mt-2">
        <div v-if="['DATE', 'DATETIME'].includes(dtype)">
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="inputDate" />
        </div>
        <div v-if="['YEAR', 'NUMBER', 'INTEGER'].includes(dtype)">
            <input type="text" v-model="inputNumber"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
        </div>
        <div v-if="['BOOLEAN', 'ARRAY', 'STRING'].includes(dtype)">
            <textarea v-model="inputString"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
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
import VueTailwindDatepicker from "vue-tailwind-datepicker"
import { INode, ITerm, IValueType, IAnswer, IAnswerResponse } from "@/interfaces"
import { isNumeric } from "@/utilities"

const { t } = useI18n()
const dtype = ref("STRING" as IValueType)
const draft = ref({} as IAnswerResponse)
const validated = ref(false)
const terms = ref([] as ITerm[])
const inputNumber = ref()
const inputDate = ref("")
const inputString = ref("")
const inputTypes: IValueType[] = ["DATE", "DATETIME", "YEAR", "NUMBER", "INTEGER", "BOOLEAN", "ARRAY", "STRING"]
const formatter = ref({
    date: "YYYY-MM-DD",
    month: "MMM"
})

const props = defineProps<{
    node: INode,
}>()
const emit = defineEmits<{ setResponse: [draft: IAnswerResponse] }>()

// WATCHERS
watch(
    () => draft.value, () => {
        let response = { ...draft.value }
        response.validated = validate()
        emit("setResponse", response)
    },
    { deep: true }
)

watch(() => inputString.value, () => {
    if (["BOOLEAN", "ARRAY", "STRING"].includes(dtype.value)) draft.value.answer = {
        id: "VALUE",
        value: inputString.value
    }
})

watch(() => inputDate.value, () => {
    if (["DATE", "DATETIME"].includes(dtype.value)) draft.value.answer = {
        id: "VALUE",
        value: inputDate.value
    }
})

watch(() => inputNumber.value, () => {
    if (["YEAR", "NUMBER", "INTEGER"].includes(dtype.value)) draft.value.answer = {
        id: "VALUE",
        value: inputNumber.value
    }
})

// VALIDATORS
function validate(): boolean {
    if (["DATE", "DATETIME"].includes(dtype.value)) {
        if (!inputDate.value) return false
    }
    if (["YEAR", "NUMBER", "INTEGER"].includes(dtype.value)) {
        if (inputNumber.value && !isNumeric(inputNumber.value)) return false
        if (
            inputNumber.value
            && props.node.form
            && props.node.form.constraints
            && (
                (
                    props.node.form.constraints.minimum
                    && inputNumber.value < props.node.form.constraints.minimum
                )
                || (
                    props.node.form.constraints.maximum
                    && inputNumber.value > props.node.form.constraints.maximum
                )
            )
        ) return false
        if (
            props.node.form
            && props.node.form.constraints
            && props.node.form.constraints.dtype
            && props.node.form.constraints.dtype === "YEAR"
            && inputNumber.value.length > 4
        ) return false
        if (!inputNumber.value) return false
    }
    if (["BOOLEAN", "ARRAY", "STRING"].includes(dtype.value)) {
        if (!inputString.value) return false
    }
    return true
}

// SETTERS
function resetDraft() {
    // Setup Term[]
    if (props.node.form && props.node.form.terms && props.node.form.terms.length)
        terms.value = [...props.node.form.terms]
    // Setup AnswerResponse
    let initialDraft = {} as IAnswerResponse
    if (props.node.response
        && Object.keys(props.node.response).length
        && props.node.response.answer
    ) {
        initialDraft = {
            answer: { ...props.node.response.answer }
        }

    }
    if (Object.keys(initialDraft).length === 0) {
        initialDraft = {
            answer: {} as IAnswer,
        }
    }
    if (
        props.node.form
        && props.node.form.constraints
        && props.node.form.constraints.dtype
        && inputTypes.includes(props.node.form.constraints.dtype)
    ) dtype.value = props.node.form.constraints.dtype
    if (
        initialDraft.answer
        && !Array.isArray(initialDraft.answer)
        && Object.keys(initialDraft.answer).length
        && dtype.value
    ) {
        if (["DATE", "DATETIME"].includes(dtype.value)) inputDate.value = initialDraft.answer.value as string
        if (["YEAR", "NUMBER", "INTEGER"].includes(dtype.value)) inputNumber.value = initialDraft.answer.value as string
        if (["BOOLEAN", "ARRAY", "STRING"].includes(dtype.value)) inputString.value = initialDraft.answer.value as string
    }
    draft.value = { ...initialDraft }
    validated.value = validate()
}
onMounted(async () => {
    resetDraft()
})
</script>