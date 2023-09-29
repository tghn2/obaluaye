<template>
    <div v-if="initialised">
        <div class="border-t border-gray-500 mt-2">
            <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6 my-2">
                <div class="col-span-2">
                    <InputValue :input-select="scaleStart" :initial-choice="scaleStartChoice"
                        @set-select="watchScaleStart" />
                </div>
                <div class="col-span-2 flex items-center justify-center font-medium text-gray-900">
                    {{ t("form.scaleTo") }}
                </div>
                <div class="col-span-2">
                    <InputValue :input-select="scaleEnd" :initial-choice="scaleEndChoice" @set-select="watchScaleEnd" />
                </div>
                <div class="col-span-1 flex items-center font-medium text-gray-900">
                    {{ scaleStartChoice }}
                </div>
                <div class="col-span-5">
                    <input type="text" name="scale-start-label" id="scale-start-label" v-model="scaleStartLabel"
                        :placeholder="`${t('form.scaleLabel')}`"
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                </div>
                <div class="col-span-1 flex items-center font-medium text-gray-900">
                    {{ scaleEndChoice }}
                </div>
                <div class="col-span-5">
                    <input type="text" name="scale-end-label" id="scale-end-label" v-model="scaleEndLabel"
                        :placeholder="`${t('form.scaleLabel')}`"
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                </div>
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
import { IForm, IConstraints, ITerm, INodeType, IValueType } from "@/interfaces"
import { generateUUID } from "@/utilities"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const draft = ref({} as IForm)
const formEditType: INodeType = "SCALE"
const defaultType: IValueType = "INTEGER"
const scaleStart: number[] = [0, 1]
const scaleEnd: number[] = [2, 3, 4, 5, 6, 7, 8, 9, 10]
const scaleStartChoice = ref(1)
const scaleStartLabel = ref("")
const scaleEndChoice = ref(5)
const scaleEndLabel = ref("")
const initialised = ref(false)

const props = defineProps<{
    initialDraft: IForm
}>()
const emit = defineEmits<{ setDraft: [draft: IForm] }>()

// WATCHERS
watch(() => [scaleStartChoice, scaleStartLabel, scaleEndChoice, scaleEndLabel], () => {
    draft.value = setDraft({ ...draft.value })
})

watch(
    () => draft.value, () => {
        const response = setDraft({ ...draft.value })
        emit("setDraft", response)
    },
    { deep: true }
)

function watchScaleStart(response: number) {
    scaleStartChoice.value = response
}
function watchScaleEnd(response: number) {
    scaleEndChoice.value = response
}

// SETTERS
function setDraft(response: IForm): IForm {
    if (response.terms && response.terms.length === 2) {
        response.terms[0].value = scaleStartChoice.value + ''
        response.terms[0].label = scaleStartLabel.value
        response.terms[1].value = scaleEndChoice.value + ''
        response.terms[1].label = scaleEndLabel.value
    }
    return response
}

function resetDraft() {
    let initialDraft = { ...props.initialDraft }
    if (Object.keys(initialDraft).length === 0 || initialDraft.formType !== formEditType) {
        initialDraft = {
            formType: formEditType,
            required: false,
            randomise: false,
            terms: [],
            constraints: {
                dtype: defaultType,
            }
        }
    }
    if (!initialDraft.required) initialDraft.required = false
    if (!initialDraft.constraints || Object.keys(initialDraft.constraints).length === 0) initialDraft.constraints = {} as IConstraints
    if (!("dtype" in initialDraft.constraints)) initialDraft.constraints.dtype = defaultType
    if (!initialDraft.terms || initialDraft.terms.length === 0) initialDraft.terms = [
        {
            id: generateUUID(),
            value: `${scaleStartChoice.value}`,
            label: "",
        },
        {
            id: generateUUID(),
            value: `${scaleEndChoice.value}`,
            label: "",
        },
    ]
    if (initialDraft.terms.length === 2) {
        scaleStartChoice.value = parseInt(initialDraft.terms[0].value as string)
        if (initialDraft.terms[0].label) scaleStartLabel.value = initialDraft.terms[0].label
        scaleEndChoice.value = parseInt(initialDraft.terms[1].value as string)
        if (initialDraft.terms[1].label) scaleEndLabel.value = initialDraft.terms[1].label
    }
    draft.value = { ...initialDraft }
    initialised.value = true
}

onMounted(async () => {
    resetDraft()
})
</script>