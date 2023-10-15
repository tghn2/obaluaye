<template>
    <fieldset class="mt-2">
        <div v-if="dtype === 'DATE'" class="flex space-x-4 items-center">
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateFrom" />
            <span class="text-gray-600">{{ t("filter.to") }}</span>
            <vue-tailwind-datepicker :formatter="formatter" as-single v-model="dateTo" />
        </div>
        <div v-else class="flex space-x-4 items-center">
            <input type="text" v-model="minimum"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-kashmir-600 sm:text-sm sm:leading-6" />
            <span class="text-gray-600">{{ t("filter.to") }}</span>
            <input type="text" v-model="maximum"
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
const dtype = ref("NUMBER" as IValueType)
const draft = ref({} as IAnswerResponse)
const validated = ref(false)
const terms = ref([] as ITerm[])
const inputTypes: IValueType[] = ["DATE", "DATETIME"]
const minimum = ref()
const maximum = ref()
const dateFrom = ref("")
const dateTo = ref("")
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

watch(() => [dateFrom.value, dateTo.value], () => {
    if (dtype.value === "DATE") draft.value.answer = [
        {
            id: "FROM",
            value: dateFrom.value
        },
        {
            id: "TO",
            value: dateTo.value
        }
    ]
})

watch(() => [minimum.value, maximum.value], () => {
    if (dtype.value === "NUMBER") draft.value.answer = [
        {
            id: "FROM",
            value: minimum.value
        },
        {
            id: "TO",
            value: maximum.value
        }
    ]
})

// VALIDATORS
function validate(): boolean {
    if (dtype.value === "DATE") {
        if (
            dateFrom.value &&
            dateTo.value
            && dateFrom.value >= dateTo.value
        ) return false
        if (!dateFrom.value && !dateTo.value) return false
    }
    if (dtype.value === "NUMBER") {
        if (
            minimum.value &&
            maximum.value
            && minimum.value >= maximum.value
        ) return false
        if (minimum.value && !isNumeric(minimum.value)) return false
        if (
            minimum.value
            && props.node.form
            && props.node.form.constraints
            && (
                (
                    props.node.form.constraints.minimum
                    && minimum.value < props.node.form.constraints.minimum
                )
                || (
                    props.node.form.constraints.maximum
                    && minimum.value > props.node.form.constraints.maximum
                )
            )
        ) return false
        if (maximum.value && !isNumeric(maximum.value)) return false
        if (
            maximum.value
            && props.node.form
            && props.node.form.constraints
            && (
                (
                    props.node.form.constraints.minimum
                    && maximum.value < props.node.form.constraints.minimum
                )
                || (
                    props.node.form.constraints.maximum
                    && maximum.value > props.node.form.constraints.maximum
                )
            )
        ) return false
        if (
            props.node.form
            && props.node.form.constraints
            && props.node.form.constraints.dtype
            && props.node.form.constraints.dtype === "YEAR"
            && (
                maximum.value.length > 4
                || minimum.value.length > 4
            )
        ) return false
        if (!minimum.value && !maximum.value) return false
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
    if (
        props.node.response
        && Object.keys(props.node.response).length
        && props.node.response.answer
    ) {
        if (
            Array.isArray(props.node.response.answer)
            && props.node.response.answer.length === 2
        ) {
            initialDraft = {
                answer: [...props.node.response.answer]
            }
        } else if (Object.values(props.node.response.answer).length === 2) {
            initialDraft = {
                answer: [...Object.values(props.node.response.answer)]
            }
        }
        if (Array.isArray(initialDraft.answer) && initialDraft.answer.length === 2) {
            minimum.value = initialDraft.answer[0].value
            maximum.value = initialDraft.answer[1].value
        }
    }
    if (Object.keys(initialDraft).length === 0) {
        initialDraft = {
            answer: [] as IAnswer[],
        }
    }
    if (
        props.node.form
        && props.node.form.constraints
        && props.node.form.constraints.dtype
        && inputTypes.includes(props.node.form.constraints.dtype)
    ) {
        dtype.value = "DATE"
        if (Array.isArray(initialDraft.answer) && initialDraft.answer.length === 2) {
            dateFrom.value = initialDraft.answer[0].value as string
            dateTo.value = initialDraft.answer[1].value as string
        }
    }
    draft.value = { ...initialDraft }
    validated.value = validate()
}
onMounted(async () => {
    resetDraft()
})
</script>