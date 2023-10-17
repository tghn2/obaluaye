<template>
    <fieldset class="mt-2">
        <div v-if="terms.length" class="mt-3 space-y-2">
            <div v-for="term in terms" :key="`node-${props.node.id}-${term.id}`" class="flex items-center gap-x-3">
                <input :id="term.id" :value="term.id" type="radio" v-model="answerID"
                    class="h-4 w-4 border-gray-300 text-kashmir-600 focus:ring-kashmir-600" />
                <label :for="term.id" class="block text-sm font-medium leading-6 text-gray-900">{{ term.value }}</label>
            </div>
        </div>
    </fieldset>
</template>

<script setup lang="ts">
import { INode, ITerm, IAnswer, IAnswerResponse } from "@/interfaces"
import { shuffle } from "@/utilities"

const { t } = useI18n()
const draft = ref({} as IAnswerResponse)
const validated = ref(false)
const answerID = ref("")
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
    // Setup Term[] - BOOLEAN, so always the same
    terms.value = [
        {
            id: "TRUE",
            value: t("form.booleanTrue")
        },
        {
            id: "FALSE",
            value: t("form.booleanFalse")
        }
    ]
    if (props.node.form && props.node.form.randomise) terms.value = shuffle(terms.value)
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