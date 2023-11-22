<template>
    <div class="m-2">
        <div class="flex-auto ring-1 ring-kashmir-500 p-1 rounded-md">
            <div class="flex-auto text-sm text-gray-500">
                <dl>
                    <div v-if="props.node.question"
                        class="flex justify-between items-center py-1 sm:px-1 text-sm font-medium leading-6 text-gray-900">
                        <span>{{ props.node!.order as number + 1 }}. {{ props.node.question }}</span>
                    </div>
                    <div v-if="props.node.subjects && props.node.subjects.length"
                        class="group flex flex-row items-center text-xs font-medium text-gray-700">
                        <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                        <span class="ml-1">
                            {{ props.node.subjects.join(", ") }}
                        </span>
                    </div>
                    <div class="py-1 sm:px-1 mt-2 border-t border-kashmir-100">
                        <component :is="formType[props.node.formType as INodeType].component" :form="props.node.form" :response="props.node.response" />
                    </div>
                    <div v-if="props.node.resources && props.node.resources.length" class="py-1 sm:px-1">
                        <ResourceViewDisclosureCard :resources="props.node.resources" />
                    </div>
                </dl>
            </div>
        </div>
    </div>
</template>
  
<script setup lang="ts">
import { PhTag } from "@phosphor-icons/vue"
import { INode, IKeyable, INodeType } from "@/interfaces"

const { t } = useI18n()
const props = defineProps<{
    node: INode,
}>()

const formType: IKeyable = {
    VALUE: { name: "form.types.value", component: resolveComponent("FormViewValueType") },
    VALUERANGE: { name: "form.types.valuerange", component: resolveComponent("FormViewValueRangeType") },
    SCALE: { name: "form.types.scale", component: resolveComponent("FormViewScaleType") },
    BOOLEAN: { name: "form.types.boolean", component: resolveComponent("FormViewBooleanType") },
    SELECTONE: { name: "form.types.selectone", component: resolveComponent("FormViewSelectOneType") },
    SELECTMANY: { name: "form.types.selectmany", component: resolveComponent("FormViewSelectManyType") },
    SELECTBRANCH: { name: "form.types.selectbranch", component: resolveComponent("FormViewSelectBranchType") },
    UPLOAD: { name: "form.types.upload", component: resolveComponent("FormViewUploadType") },
}
</script>