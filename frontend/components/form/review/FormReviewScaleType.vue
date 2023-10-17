<template>
    <fieldset v-if="terms.length" class="flex items-center gap-x-1 text-sm leading-6 px-2 mt-5 justify-center">
        <label v-if="labels.length === 2" class="block text-sm font-medium leading-6 text-gray-900">{{ labels[0] }}</label>
        <div v-for="term in terms" :key="`node-${props.node.id}-${term.id}`"
            class="group flex items-center gap-x-1 text-sm leading-6 px-2">
            <PhCircle :class="[term.selected ? 'text-kashmir-600' : 'text-gray-400', 'h-4 w-4 shrink-0']"
                :weight="term.selected ? 'duotone' : 'regular'" aria-hidden="true" />
            <span :class="[term.selected ? 'text-kashmir-600 font-bold' : 'text-gray-900', 'text-sm']">
                {{ term.value }}
            </span>
        </div>
        <label v-if="labels.length === 2" class="block text-sm font-medium leading-6 text-gray-900">{{ labels[1] }}</label>
    </fieldset>
</template>

<script setup lang="ts">
import { PhCircle } from "@phosphor-icons/vue"
import { INode, IKeyable } from "@/interfaces"

const terms = ref([] as IKeyable[])
const labels = ref([] as string[])

const props = defineProps<{
    node: INode,
}>()

// SETTERS
function setReview() {
    // Setup Term[]
    if (props.node.form && props.node.form.terms && props.node.form.terms.length === 2) {
        labels.value = [
            props.node.form.terms[0].label ? props.node.form.terms[0].label : '',
            props.node.form.terms[1].label ? props.node.form.terms[1].label : '',
        ]
        let selection = ""
        if (props.node.response && Object.keys(props.node.response).length && props.node.response.answer)
            selection = props.node.response.answer.id
        terms.value = [] as IKeyable[]
        for (let i = parseInt(props.node.form.terms[0].value as string); i <= parseInt(props.node.form.terms[1].value as string); i++)
            terms.value.push(
                {
                    id: i + '',
                    value: i + '',
                    selected: selection === i + ''
                }
            )
    }
}

onMounted(async () => {
    setReview()
})
</script>
