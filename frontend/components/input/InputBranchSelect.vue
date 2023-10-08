<template>
    <Listbox v-model="branch" id="form-selection-types">
        <div class="relative mt-1">
            <ListboxButton
                class="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus-visible:border-kashmir-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-kashmir-300 sm:text-sm">
                <span v-if="branch" class="block truncate text-gray-900">
                    <!-- @vue-ignore -->
                    <!-- @vue-expect-error -->
                    {{ branchList.find((b: IKeyable) => b.id === branch).name }}
                </span>
                <span v-else class="block truncate text-gray-900">
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
                    <ListboxOption v-slot="{ active, selected }" v-for="theme in branchList" :key="`theme-${theme.id}`"
                        :value="theme.id" as="template">
                        <li :class="[
                            active ? 'bg-kashmir-100 text-kashmir-900' : 'text-gray-900',
                            'relative cursor-default select-none py-2 pl-10 pr-4',
                        ]">
                            <span :class="[
                                selected ? 'font-medium' : 'font-normal',
                                'block truncate',
                            ]">{{ theme.name }}</span>
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
import { usePathwayStore } from "@/stores"
import { IKeyable } from "@/interfaces"

const { t } = useI18n()
const pathwayStore = usePathwayStore()
const branch = ref("")
const branchList = ref([] as IKeyable[])

const props = defineProps<{
    initialBranch?: string,
    termId: string,
    themeId: string,
}>()
const emit = defineEmits<{
    setSelect: [select: string]
}>()

// WATCHERS
watch(
    () => branch.value, () => {
        emit("setSelect", `${props.termId}|${branch.value}`)
    }
)

watch(
    () => pathwayStore.draft.themes, () => {
        setBranchList()
    }
)

// SETTERS
onMounted(async () => {
    if (props.initialBranch) branch.value = props.initialBranch
    setBranchList()
})

function setBranchList() {
    branchList.value = []
    if (pathwayStore.draft!.themes) {
        for (const theme of pathwayStore.draft!.themes) {
            if (theme.id !== props.themeId) branchList.value.push({
                id: theme.id,
                name: theme.title
            })
        }
    }
    if (!branchList.value.length) branchList.value = [
        {
            id: "",
            name: t("form.branchNone")
        }
    ]
}

</script>