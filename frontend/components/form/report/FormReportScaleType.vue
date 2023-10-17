<template>
    <fieldset v-if="terms.length" class="flex items-center gap-x-1 text-sm leading-6 px-2 mt-5 justify-center">
        <label v-if="labels.length === 2" class="block text-sm font-medium leading-6 text-gray-900">{{ labels[0] }}</label>
        <div v-for="term in terms" :key="`node-${props.node.id}-${term.id}`"
            class="group flex items-center gap-x-1 text-sm leading-6 px-2">
            <input :id="term.id" :value="term.id" type="radio" v-model="answerID"
                class="h-4 w-4 border-gray-300 text-kashmir-600 focus:ring-kashmir-600" />
            <label :for="term.id" class="block text-sm ml-1 font-medium leading-6 text-gray-900">{{ term.value }}</label>
        </div>
        <label v-if="labels.length === 2" class="block text-sm font-medium leading-6 text-gray-900">{{ labels[1] }}</label>
    </fieldset>
</template>

<script setup lang="ts">
import { INode, ITerm, IAnswer, IAnswerResponse } from "@/interfaces"

const draft = ref({} as IAnswerResponse)
const validated = ref(false)
const answerID = ref("")
const terms = ref([] as ITerm[])
const labels = ref([] as string[])

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

watch(() => [answerID.value], () => {
    setChoice(answerID.value)
})

// GETTERS
function getTerm(termID: string) {
    return terms.value.find(
        (term: ITerm) => term.id === termID
    )
}

function getTermIndex(termID: string) {
    return terms.value.findIndex(
        (term: ITerm) => term.id === termID
    )
}

// VALIDATORS
function validate(): boolean {
    if (draft.value && draft.value.answer && !Array.isArray(draft.value.answer) && Object.keys(draft.value.answer).length !== 0) {
        const termIdx = getTermIndex(draft.value.answer.id as string)
        if (termIdx >= 0) return true
    }
    return false
}

// SETTERS
function setChoice(answer: string) {
    let choice = getTerm(answer) as ITerm
    if (choice) draft.value.answer = {
        id: choice.id,
        value: choice.value
    }
    validated.value = validate()
}

function resetDraft() {
    // Setup Term[]
    if (props.node.form && props.node.form.terms && props.node.form.terms.length === 2) {
        labels.value = [
            props.node.form.terms[0].label ? props.node.form.terms[0].label : '',
            props.node.form.terms[1].label ? props.node.form.terms[1].label : '',
        ]
        terms.value = [] as ITerm[]
        for (let i = parseInt(props.node.form.terms[0].value as string); i <= parseInt(props.node.form.terms[1].value as string); i++)
            terms.value.push(
                {
                    id: i + '',
                    value: i + ''
                }
            )
    }
    // Setup AnswerResponse
    let initialDraft = {} as IAnswerResponse
    if (props.node.response && Object.keys(props.node.response).length && props.node.response.answer) {
        initialDraft = {
            answer: { ...props.node.response.answer }
        }
    }
    if (Object.keys(initialDraft).length === 0) {
        initialDraft = {
            answer: {} as IAnswer,
        }
    }
    draft.value = { ...initialDraft }
    if (initialDraft && initialDraft.answer && !Array.isArray(initialDraft.answer) && initialDraft.answer.id) answerID.value = initialDraft.answer.id
    validated.value = validate()
}

onMounted(async () => {
    resetDraft()
})
</script>
