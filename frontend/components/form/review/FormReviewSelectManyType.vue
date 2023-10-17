<template>
    <fieldset class="mt-2">
        <div v-if="terms.length" class="mt-3 space-y-2">
            <div v-for="term in terms" :key="`node-${props.node.id}-${term.id}`" class="flex items-center gap-x-3">
                <div class="group flex items-center gap-x-1 text-sm leading-6 px-2">
                    <PhSquare :class="[term.selected ? 'text-kashmir-600' : 'text-gray-400', 'h-4 w-4 shrink-0']"
                        :weight="term.selected ? 'duotone' : 'regular'" aria-hidden="true" />
                    <span :class="[term.selected ? 'text-kashmir-600 font-bold' : 'text-gray-900', 'text-sm']">
                        {{ term.value }}
                    </span>
                </div>
            </div>
        </div>
    </fieldset>
</template>

<script setup lang="ts">
import { PhSquare } from "@phosphor-icons/vue"
import { INode, ITerm, IKeyable } from "@/interfaces"

const terms = ref([] as IKeyable[])

const props = defineProps<{
    node: INode,
}>()

// GETTERS
function getTermIndex(termID: string) {
    return terms.value.findIndex(
        (term: ITerm) => term.id === termID
    )
}

// SETTERS
function setReview() {
    // Setup Term[]
    terms.value = []
    if (props.node.form && props.node.form.terms && props.node.form.terms.length)
        for (const term of props.node.form.terms) {
            terms.value.push({
                id: term.id,
                value: term.value,
                selected: false
            })
        }
    // Set answer response
    let answerList: IKeyable[] = []
    if (
        props.node.response
        && Object.keys(props.node.response).length
        && props.node.response.answer
    ) {
        if (
            Array.isArray(props.node.response.answer)
            && props.node.response.answer.length
        ) {
            answerList = [...props.node.response.answer]
        } else {
            answerList = [...Object.values(props.node.response.answer)]
        }
    }
    for (const answer of answerList) {
        const termIdx = getTermIndex(answer.id)
        if (termIdx >= 0) terms.value[termIdx].selected = true
    }
}

onMounted(async () => {
    setReview()
})
</script>