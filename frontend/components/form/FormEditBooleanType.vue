<template>
    <div class="border-t border-gray-500 mt-2">
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
import { IForm, IConstraints, INodeType, IValueType } from "@/interfaces"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const draft = ref({} as IForm)
const formEditType: INodeType = "BOOLEAN"
const defaultType: IValueType = "BOOLEAN"

const props = defineProps<{
    initialDraft: IForm,
}>()
const emit = defineEmits<{ setDraft: [draft: IForm] }>()

// WATCHERS
watch(
    () => draft.value, () => {
        const response = setDraft({ ...draft.value })
        emit("setDraft", response)
    },
    { deep: true }
)

// SETTERS
function setDraft(response: IForm): IForm {
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
    draft.value = { ...initialDraft }
}

onMounted(async () => {
    resetDraft()
})
</script>