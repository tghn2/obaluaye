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
                <div class="col-span-3 flex items-center">
                    <span v-if="draft.terms && draft.terms.length" class="font-medium text-gray-900 mr-2">{{
                        t("form.constraints.limit")
                    }}</span>
                    <Listbox v-if="draft.terms && draft.terms.length" v-model="manyLimit" id="form-selection-types">
                        <div class="relative mt-1">
                            <ListboxButton
                                class="relative w-24 cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus-visible:border-spring-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-spring-300 sm:text-sm">
                                <span class="block truncate text-gray-900">
                                    {{ manyLimit }}
                                </span>
                                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                    <PhCaretUpDown class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                </span>
                            </ListboxButton>
                            <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                                leave-to-class="opacity-0">
                                <ListboxOptions
                                    class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                    <ListboxOption v-slot="{ active, selected }"
                                        v-for="itype in [...Array(draft.terms.length).keys()]" :key="`itype-${itype}`"
                                        :value="itype + 1" as="template">
                                        <li :class="[
                                            active ? 'bg-spring-100 text-spring-900' : 'text-gray-900',
                                            'relative cursor-default select-none py-2 pl-10 pr-4',
                                        ]">
                                            <span :class="[
                                                selected ? 'font-medium' : 'font-normal',
                                                'block truncate',
                                            ]">{{ itype + 1 }}</span>
                                            <span v-if="selected"
                                                class="absolute inset-y-0 left-0 flex items-center pl-3 text-spring-600">
                                                <PhCheck class="h-5 w-5" aria-hidden="true" />
                                            </span>
                                        </li>
                                    </ListboxOption>
                                </ListboxOptions>
                            </transition>
                        </div>
                    </Listbox>
                </div>
                <div class="col-span-3 flex justify-end">
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
import { PhX, PhPlus, PhCaretUpDown, PhCheck } from "@phosphor-icons/vue"
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, Switch, SwitchGroup, SwitchLabel } from "@headlessui/vue"
import { usePathwayStore } from "@/stores"
import { IForm, IConstraints, ITerm, INodeType, IValueType } from "@/interfaces"
import { generateUUID } from "@/utilities"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const draft = ref({} as IForm)
const formEditType: INodeType = "SELECTMANY"
const defaultType: IValueType = "STRING"
const manyLimit = ref(1)

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
watch(() => [manyLimit], () => {
    draft.value = setDraft({ ...draft.value })
})

watch(
    () => draft.value, () => {
        const response = setDraft({ ...draft.value })
        emit("setDraft", response)
    },
    { deep: true }
)

// SETTERS
function setDraft(response: IForm): IForm {
    if (manyLimit.value && manyLimit.value > 0 && manyLimit.value <= response.terms!.length) response.constraints!.limit = manyLimit.value
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
    if (initialDraft.constraints.limit) manyLimit.value = initialDraft.constraints.limit
    draft.value = { ...initialDraft }
}

onMounted(async () => {
    resetDraft()
})
</script>