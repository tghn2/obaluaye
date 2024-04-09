<template>
    <Listbox v-model="choices" id="country-selection-codes" :multiple="collection.isMulti">
        <div class="relative mt-1">
            <ListboxButton
                class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus-visible:border-kashmir-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-kashmir-300 sm:text-sm">
                <span v-if="choices && choices.length" class="block truncate text-gray-900">
                    {{ getTermString() }}
                </span>
                <span v-else class="block truncate text-gray-500">
                    {{ t("form.select") }}
                </span>
                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <PhCaretUpDown class="h-5 w-5 text-gray-400" aria-hidden="true" />
                </span>
            </ListboxButton>
            <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                leave-to-class="opacity-0">
                <ListboxOptions
                    class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="choice in selectionChoices" :key="`selection-choice-${choice.id}`"
                        :value="choice.id" as="template">
                        <li :class="[
                            active ? 'bg-kashmir-100 text-kashmir-900' : 'text-gray-900',
                            'relative cursor-default select-none py-2 pl-10 pr-4',
                        ]">
                            <span :class="[
                                selected ? 'font-medium' : 'font-normal',
                                'block truncate',
                            ]">{{ choice.term }}</span>
                            <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-kashmir-600">
                                <PhCheck class="h-5 w-5" aria-hidden="true" />
                            </span>
                        </li>
                    </ListboxOption>
                </ListboxOptions>
            </transition>
        </div>
    </Listbox>
</template>
  
<script setup lang="ts">
import { PhCaretUpDown, PhCheck } from "@phosphor-icons/vue"
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, } from "@headlessui/vue"
import { ISelection, ICollection, IKeyable } from "@/interfaces"
import { useSettingStore } from "@/stores"

const { t } = useI18n()
const choices = ref<string | string[]>([] as string[])
const originalChoices = ref([] as string[])
const selectionChoices = ref([] as ISelection[])
const selectionChoiceIds = ref([] as string[])
const settingStore = useSettingStore()

const props = defineProps<{
    allSelections?: string[],
    collection: ICollection,
}>()
const emit = defineEmits<{
    setSelection: [selection: IKeyable]
}>()

// WATCHERS
watch(
    () => settingStore.currentLocale, () => setSelectionChoices(),
)

watch(
    () => choices.value, () => {
        let tempOriginal = [...originalChoices.value]
        if (Array.isArray(choices.value)) {
            originalChoices.value = [...choices.value]
            emit("setSelection", {
                original: [...tempOriginal],
                choices: [...choices.value]
            })
        }
        else {
            originalChoices.value = [choices.value]
            emit("setSelection", {
                original: [...tempOriginal],
                choices: [choices.value]
            })
        }
    }
)

function getTermString(): string {
    if (Array.isArray(choices.value)) {
        let filtered = selectionChoices.value.filter((slctn) => choices.value.includes(slctn.id as string))
        if (filtered.length) return filtered.map(({term}) => term).join(', ')
    } else {
        let filtered = selectionChoices.value.find((slctn) => slctn.id as string === choices.value)
        if (filtered) return filtered.term as string
    }
    return t("form.select")
}

// SETTERS
onMounted(async () => {
    // there is a problem ... doesn't react
    await new Promise(r => setTimeout(r, 100))
    setSelectionChoices()
})

function setSelectionChoices() {
    if (props.collection.selection && props.collection.selection.length) {
        selectionChoices.value = [...props.collection.selection]
        // https://stackoverflow.com/a/1129270/295606
        // @ts-ignore
        selectionChoices.value.sort((a, b) => (a.term > b.term) ? 1 : ((b.term > a.term) ? -1 : 0))
        // @ts-ignore
        selectionChoiceIds.value = selectionChoices.value.map(({ id }) => id)
        if (props.allSelections && props.allSelections.length) {
            // https://stackoverflow.com/a/46694321/295606
            originalChoices.value = props.allSelections.filter(i => selectionChoiceIds.value.includes(i))
            if (originalChoices.value.length) {
                if (props.collection.isMulti) choices.value = [...originalChoices.value]
                else choices.value = originalChoices.value[0]
            }
        }
    }
}
</script>