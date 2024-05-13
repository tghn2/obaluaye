<template>
    <div class="flex-auto ring-1 ring-kashmir-500 m-2 p-1 rounded-md">
        <div class="flex-auto text-sm text-gray-500">
            <dl>
                <div v-if="props.node.question"
                    class="flex justify-between items-center py-1 sm:px-1 text-sm font-medium leading-6 text-gray-900">
                    <span>{{ props.node!.order as number + 1 }}. {{ props.node.question }}</span>
                    <PhCheckCircle v-if="validated"
                        class="text-spring-500 bg-spring-100 rounded-full p-0.5 h-6 w-6 shrink-0" aria-hidden="true" />
                    <PhWarningCircle v-else :class="[
                        props.node.form && props.node.form?.required
                            ? 'text-cerise-500 bg-cerise-100'
                            : 'text-gray-700', 'rounded-full p-0.5 h-6 w-6 shrink-0'
                    ]" aria-hidden="true" />
                </div>
                <div v-if="props.node.subjects && props.node.subjects.length"
                    class="group flex flex-row items-center text-xs font-medium text-gray-700">
                    <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span class="ml-1">
                        {{ props.node.subjects.join(", ") }}
                    </span>
                </div>
                <div class="py-1 sm:px-1 mt-2 border-t border-kashmir-100">
                    <component :is="formType[props.node.formType as INodeType].component" :node="props.node"
                        @set-response="watchResponseUpdate" />
                </div>
                <div v-if="props.node.resources && props.node.resources.length" class="py-1 sm:px-1">
                    <ResourceViewDisclosureCard :resources="props.node.resources" :start-open="false" />
                </div>
            </dl>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PhTag, PhArrowSquareOut, PhCheckCircle, PhWarningCircle } from "@phosphor-icons/vue"
import { INode, IKeyable, INodeType, IResponse, IAnswer, IAnswerResponse } from "@/interfaces"
import { generateUUID } from "@/utilities"

const { t } = useI18n()
const props = defineProps<{
    node: INode,
}>()
const emit = defineEmits<{ setResponse: [draft: IResponse] }>()

const draft = ref({} as IResponse)
const validated = ref(false)
const formType: IKeyable = {
    VALUE: { name: "form.types.value", component: resolveComponent("FormResponseValueType") },
    VALUERANGE: { name: "form.types.valuerange", component: resolveComponent("FormResponseValueRangeType") },
    SCALE: { name: "form.types.scale", component: resolveComponent("FormResponseScaleType") },
    BOOLEAN: { name: "form.types.boolean", component: resolveComponent("FormResponseBooleanType") },
    SELECTONE: { name: "form.types.selectone", component: resolveComponent("FormResponseSelectOneType") },
    SELECTMANY: { name: "form.types.selectmany", component: resolveComponent("FormResponseSelectManyType") },
    SELECTBRANCH: { name: "form.types.selectbranch", component: resolveComponent("FormResponseSelectBranchType") },
    UPLOAD: { name: "form.types.upload", component: resolveComponent("FormResponseUploadType") },
}

// WATCHERS
function watchResponseUpdate(response: IAnswerResponse) {
    if (response.validated) {
        validated.value = true
    } else validated.value = false
    draft.value.answer = { ...response.answer }
    draft.value.validated = validated.value
    emit("setResponse", { ...draft.value })
}

// SETTERS
function resetDraft() {
    draft.value = {} as IResponse
    if (props.node.response && Object.keys(props.node.response).length) {
        draft.value = { ...props.node.response }
    }
    if (Object.keys(draft.value).length === 0) {
        draft.value = {
            id: generateUUID(),
            node_id: props.node.id,
            answer: {} as IAnswer,
        }
    }
}

onMounted(async () => {
    resetDraft()
})
</script>