<template>
    <fieldset class="mt-2">
        <div v-if="terms.length" class="mt-3 space-y-2">
            <div v-for="term in terms" :key="`node-${props.node.id}-${term.id}`" class="flex items-center gap-x-3">
                <input :id="term.id" :value="term.id" type="checkbox" v-model="answerID"
                    class="h-4 w-4 border-gray-300 text-kashmir-600 focus:ring-kashmir-600" />
                <label :for="term.id" class="block text-sm font-medium leading-6 text-gray-900">{{ term.value }}</label>
            </div>
        </div>
        <p v-if="props.node.form && props.node.form.constraints && props.node.form.constraints.limit"
            class="mt-2 text-sm leading-6 text-gray-500">
            {{ t("form.constraints.maximum") }}: {{ props.node.form.constraints.limit }}
        </p>
    </fieldset>
</template>

<script setup lang="ts">
import { INode, ITerm, IAnswer, IAnswerResponse } from "@/interfaces"
import { shuffle } from "@/utilities"

const { t } = useI18n()
const draft = ref({} as IAnswerResponse)
const validated = ref(false)
const answerID = ref([] as string[])
const terms = ref([] as ITerm[])

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
    if (draft.value.answer
        && props.node.form
        && props.node.form.constraints
        && props.node.form.constraints.limit
        && Array.isArray(draft.value.answer)
        && draft.value.answer.length > props.node.form.constraints.limit) return false
    if (draft.value.answer
        && props.node.form
        && props.node.form.constraints
        && props.node.form.constraints.limit
        && Array.isArray(draft.value.answer)
        && draft.value.answer.length) for (const answer of draft.value.answer) {
            const termIdx = getTermIndex(answer.id as string)
            if (termIdx < 0) return false
        }
    return true
}

// SETTERS
function setChoice(answerList: string[]) {
    let answerChoice = [] as IAnswer[]
    for (const answer of answerList) {
        const choice = getTerm(answer) as ITerm
        if (choice) answerChoice.push({ ...choice })
    }
    draft.value.answer = [...answerChoice]
    validated.value = validate()
}

function resetDraft() {
    // Setup Term[]
    if (props.node.form && props.node.form.terms && props.node.form.terms.length)
        terms.value = [...props.node.form.terms]
    if (props.node.form && props.node.form.randomise) terms.value = shuffle(terms.value)
    // Setup AnswerResponse
    let initialDraft = {} as IAnswerResponse
    if (
        props.node.response
        && Object.keys(props.node.response).length
        && props.node.response.answer
    ) {
        if (
            Array.isArray(props.node.response.answer)
            && props.node.response.answer.length
        ) {
            initialDraft = {
                answer: [...props.node.response.answer]
            }
        } else {
            initialDraft = {
                answer: [...Object.values(props.node.response.answer)]
            }
        }
    }
    if (Object.keys(initialDraft).length === 0) {
        initialDraft = {
            answer: [] as IAnswer[],
        }
    }
    draft.value = { ...initialDraft }
    answerID.value = [] as string[]
    if (initialDraft && initialDraft.answer && Array.isArray(initialDraft.answer) && initialDraft.answer.length) for (const answer of initialDraft.answer) {
        answerID.value.push(answer.id as string)
    }
    validated.value = validate()
}

onMounted(async () => {
    resetDraft()
})
</script>