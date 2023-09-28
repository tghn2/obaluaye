<template>
    <div class="border-t border-gray-500 mt-2">
        <div class="mt-2">
            <table class="min-w-full divide-y divide-gray-200">
                <tbody class="divide-y divide-gray-200">
                    <tr v-for="(term, termIdx) in draft.terms" :key="`term-${term.id}`">
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-700">
                            <input type="text" v-model="draft.terms![termIdx].value"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-spring-600 sm:text-sm sm:leading-6" />
                        </td>
                        <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                            <button type="button" @click="removeTerm(termIdx)"
                                class="relative items-center rounded-full p-1 text-rose-700 hover:bg-rose-50">
                                <PhX class="h-5 w-5" aria-hidden="true" />
                            </button>
                        </td>
                    </tr>
                    <tr>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-700">
                            {{ t("form.new") }}
                        </td>
                        <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                            <button type="button" @click="addTerm"
                                class="relative items-center rounded-full p-1 text-spring-500 hover:bg-spring-100">
                                <PhPlus class="h-5 w-5" aria-hidden="true" />
                            </button>
                        </td>

                    </tr>
                </tbody>
            </table>
        </div>
        <div class="border-t border-gray-900/10">
            <div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
                <div class="col-span-full flex justify-end">
                    <SwitchGroup as="div" class="flex items-center p-3 mt-3 -ml-2">
                        <Switch v-model="draft.randomise"
                            class="group relative inline-flex h-5 w-10 flex-shrink-0 cursor-pointer items-center justify-center rounded-full focus:outline-none">
                            <span aria-hidden="true"
                                class="pointer-events-none absolute h-full w-full rounded-md bg-white" />
                            <span aria-hidden="true"
                                :class="[draft.randomise ? 'bg-spring-600' : 'bg-gray-200', 'pointer-events-none absolute mx-auto h-4 w-9 rounded-full transition-colors duration-200 ease-in-out']" />
                            <span aria-hidden="true"
                                :class="[draft.randomise ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none absolute left-0 inline-block h-5 w-5 transform rounded-full border border-gray-200 bg-white shadow ring-0 transition-transform duration-200 ease-in-out']" />
                        </Switch>
                        <SwitchLabel as="span" class="ml-3 text-sm">
                            <span class="font-medium text-gray-900">{{ t("form.randomise") }}</span>
                        </SwitchLabel>
                    </SwitchGroup>
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
import { PhX, PhPlus } from "@phosphor-icons/vue"
import { Switch, SwitchGroup, SwitchLabel } from "@headlessui/vue"
import { usePathwayStore } from "@/stores"
import { IForm, IConstraints, ITerm, INodeType, IValueType } from "@/interfaces"
import { generateUUID } from "@/utilities"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const draft = ref({} as IForm)
const formEditType: INodeType = "SELECTONE"
const defaultType: IValueType = "STRING"

const props = defineProps<{
    initialDraft: IForm,
}>()
const emit = defineEmits<{ setDraft: [draft: IForm] }>()

// TERMS
function addTerm(): void {
    if (!draft.value.terms) draft.value.terms = []
    const newTerm: ITerm = {
        id: generateUUID(),
        value: "",
    }
    draft.value.terms.splice(draft.value.terms.length, 1, newTerm)
}

function removeTerm(term: number): void {
    if (draft.value.terms && draft.value.terms.length) draft.value.terms.splice(term, 1)
}

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
            randomise: false,
            terms: [
                {
                    id: generateUUID(),
                    value: ""
                }
            ],
            constraints: {
                dtype: defaultType,
            }
        }
    }
    if (!initialDraft.required) initialDraft.required = false
    if (!initialDraft.randomise) initialDraft.randomise = false
    if (!initialDraft.constraints || Object.keys(initialDraft.constraints).length === 0) initialDraft.constraints = {} as IConstraints
    if (!("dtype" in initialDraft.constraints)) initialDraft.constraints.dtype = defaultType
    draft.value = { ...initialDraft }
}

onMounted(async () => {
    resetDraft()
})
</script>