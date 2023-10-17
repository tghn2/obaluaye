<template>
    <fieldset>
        <div v-if="terms.length" class="mt-3 space-y-2">
            <div v-for="term in terms" :key="`node-${props.node.id}-${term.id}`" class="flex items-center gap-x-3">
                <div class="group flex items-center gap-x-1 text-sm leading-6 px-2">
                    <PhCircle :class="[term.selected ? 'text-kashmir-600' : 'text-gray-400', 'h-4 w-4 shrink-0']"
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
import { PhCircle } from "@phosphor-icons/vue"
import { INode, ITerm, IKeyable } from "@/interfaces"

const { t } = useI18n()
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
    // Setup Term[] - BOOLEAN, so always the same
    terms.value = [
        {
            id: "TRUE",
            value: t("form.booleanTrue"),
            selected: false
        },
        {
            id: "FALSE",
            value: t("form.booleanFalse"),
            selected: false
        }
    ]
    // Set answer response
    if (props.node.response && Object.keys(props.node.response).length && props.node.response.answer) {
        const termIdx = getTermIndex(props.node.response.answer.id)
        if (termIdx >= 0) terms.value[termIdx].selected = true
    }
}

onMounted(async () => {
    setReview()
})
</script>