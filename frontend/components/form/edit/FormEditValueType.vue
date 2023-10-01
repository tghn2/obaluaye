<template>
    <div class="border-t border-gray-500 mt-2">
        <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6 my-2">
            <div class="col-span-4 flex items-center font-medium text-gray-900">
                {{ t("form.responsevalue") }}
            </div>
            <div class="col-span-2">
                <InputSelectType :input-select="inputTypes" :initial-choice="dtype" @set-select="watchInputDataType" />
            </div>
            <div v-if="['NUMBER', 'INTEGER'].includes(dtype)"
                class="col-span-4 flex items-center font-medium text-gray-900">
                {{ t("form.constraints.minimum") }}
            </div>
            <div v-if="['NUMBER', 'INTEGER'].includes(dtype)" class="col-span-2">
                <input type="text" name="constraints-minimum" id="constraints-minimum" v-model="dtypeMinimum"
                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
            </div>
            <div v-if="['NUMBER', 'INTEGER'].includes(dtype)"
                class="col-span-4 flex items-center font-medium text-gray-900">
                {{ t("form.constraints.maximum") }}
            </div>
            <div v-if="['NUMBER', 'INTEGER'].includes(dtype)" class="col-span-2">
                <input type="text" name="constraints-maximum" id="constraints-maximum" v-model="dtypeMaximum"
                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
            </div>
        </div>
        <div class="border-t border-gray-900/10">
            <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
                <div class="col-span-full flex justify-end">
                    <SwitchGroup as="div" class="flex items-center p-3 mt-3 -ml-2">
                        <Switch v-model="draft.required"
                            class="group relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer items-center justify-center rounded-full focus:outline-none">
                            <span aria-hidden="true"
                                class="pointer-events-none absolute h-full w-full rounded-md bg-white" />
                            <span aria-hidden="true"
                                :class="[draft.required ? 'bg-spring-600' : 'bg-gray-200', 'pointer-events-none absolute mx-auto h-4 w-9 rounded-full transition-colors duration-200 ease-in-out']" />
                            <span aria-hidden="true"
                                :class="[draft.required ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none absolute left-0 inline-block h-5 w-5 transform rounded-full border border-gray-200 bg-white shadow ring-0 transition-transform duration-200 ease-in-out']" />
                        </Switch>
                        <SwitchLabel as="span" class="ml-3 text-sm">
                            <span class="font-medium text-gray-900">{{ t("form.required") }}</span>
                        </SwitchLabel>
                    </SwitchGroup>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Switch, SwitchGroup, SwitchLabel } from "@headlessui/vue"
import { usePathwayStore } from "@/stores"
import { IForm, IConstraints, IValueType, INodeType } from "@/interfaces"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const draft = ref({} as IForm)
const dtype = ref("STRING" as IValueType)
const dtypeMinimum = ref()
const dtypeMaximum = ref()
const formEditType: INodeType = "VALUE"
const inputTypes: IValueType[] = ["DATE", "DATETIME", "YEAR", "NUMBER", "INTEGER", "BOOLEAN", "ARRAY", "STRING"]
const defaultType: IValueType = "STRING"

const props = defineProps<{
    initialDraft: IForm,
}>()
const emit = defineEmits<{ setDraft: [draft: IForm] }>()

// WATCHERS
watch(() => [dtypeMinimum, dtypeMaximum], () => {
    draft.value = setDraft({ ...draft.value })
})

watch(
    () => draft.value, () => {
        const response = setDraft({ ...draft.value })
        emit("setDraft", response)
    },
    { deep: true }
)

function watchInputDataType(response: IValueType) {
    if (!draft.value.constraints || Object.keys(draft.value.constraints).length === 0) draft.value.constraints = {} as IConstraints
    dtype.value = response
    draft.value.constraints.dtype = response
}

// SETTERS
function setDraft(response: IForm): IForm {
    if (dtypeMinimum.value) response.constraints!.minimum = dtypeMinimum.value
    if (dtypeMaximum.value && (!dtypeMinimum.value || dtypeMaximum.value > dtypeMinimum.value)) response.constraints!.maximum = dtypeMaximum.value
    return response
}

function resetDraft() {
    let initialDraft = { ...props.initialDraft }
    if (Object.keys(initialDraft).length === 0 || initialDraft.formType !== formEditType) {
        initialDraft = {
            formType: formEditType,
            required: false,
            terms: [],
            constraints: {
                dtype: defaultType,
            }
        }
    }
    if (!initialDraft.required) initialDraft.required = false
    if (!initialDraft.constraints || Object.keys(initialDraft.constraints).length === 0) initialDraft.constraints = {} as IConstraints
    if (!("dtype" in initialDraft.constraints)) initialDraft.constraints.dtype = defaultType
    if (initialDraft.constraints.dtype) dtype.value = initialDraft.constraints.dtype
    if (initialDraft.constraints.minimum) dtypeMinimum.value = initialDraft.constraints.minimum
    if (initialDraft.constraints.maximum) dtypeMaximum.value = initialDraft.constraints.maximum
    draft.value = { ...initialDraft }
}

onMounted(async () => {
    resetDraft()
})
</script>