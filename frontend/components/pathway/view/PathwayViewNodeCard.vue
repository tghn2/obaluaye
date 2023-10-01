<template>
    <div class="flex-auto mb-2">
        <div class="flex-auto rounded-lg text-sm text-gray-500">
            <dl>
                <div v-if="props.node.question" class="py-1 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-1">
                    <dt class="text-sm font-medium text-gray-900">{{ t("node.field.question") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{{
                        props.node.question }}
                    </dd>
                </div>
                <div v-if="props.node.subjects && props.node.subjects.length"
                    class="py-1 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-1">
                    <dt class="text-sm font-medium text-gray-900">{{ t("node.field.subjects") }}</dt>
                    <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                        {{ props.node.subjects.join(", ") }}
                    </dd>
                </div>
                <div class="py-1 sm:px-1">
                    <component :is="formType[props.node.formType as INodeType].component" :form="props.node.form" />
                </div>
            </dl>
        </div>
    </div>
</template>
  
<script setup lang="ts">
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