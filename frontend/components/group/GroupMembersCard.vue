<template>
    <div class="flex-auto p-3">
        <div class="shadow sm:rounded-md min-w-max">
            <GroupInvitationPanel v-if="groupStore.isCustodian" :group-id="props.groupId" />
            <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                            {{ t("group.members.since") }}
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                            {{ t("group.members.name") }}
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                            {{ t("group.members.email") }}
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                            {{ t("group.members.responsibility") }}
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
                        <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                    <tr v-for="member in groupStore.members" :key="member.id">
                        <td class="px-3 py-3.5 text-left text-sm text-gray-900">
                            <time :datetime="member.created">{{ readableDate(member.created as string) }}</time>
                        </td>
                        <td class="px-3 py-3.5 text-left text-sm text-gray-900">
                            {{ member.researcher.full_name }}
                        </td>
                        <td class="px-3 py-3.5 text-left text-sm text-gray-900">{{ member.researcher.email }}</td>
                        <td v-if="parameters.includes(member.responsibility) && member.researcher.email !== authStore.email"
                            class="pr-3 py-3.5 text-left text-sm  text-gray-900">
                            <Listbox>
                                <div class="relative">
                                    <ListboxButton
                                        class="relative w-full cursor-default rounded-lg py-1 pl-3 pr-10 text-left ring-1 ring-gray-400 focus:outline-none focus-visible:border-kashmir-500 focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-kashmir-300 sm:text-sm">
                                        <span class="block truncate">{{
                                            t(`group.roles.${member.responsibility.toLowerCase()}`) }}</span>
                                        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                            <PhCaretUpDown class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </span>
                                    </ListboxButton>
                                    <transition leave-active-class="transition duration-100 ease-in"
                                        leave-from-class="opacity-100" leave-to-class="opacity-0">
                                        <ListboxOptions
                                            class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md py-1 bg-white text-base shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                            <ListboxOption v-slot="{ active, selected }" v-for="rtype in parameters"
                                                :key="`rtype-${roleSelection[rtype].value}`"
                                                :value="roleSelection[rtype].value" as="template">
                                                <li :class="[
                                                    active ? 'bg-kashmir-100 text-kashmir-900' : 'text-gray-900',
                                                    'relative cursor-default select-none py-2 pl-10 pr-4',
                                                ]"
                                                    @click="updateMemberRole(member.id, roleSelection[rtype].value as IRoleType)">
                                                    <span :class="[
                                                        selected ? 'font-medium' : 'font-normal',
                                                        'block truncate',
                                                    ]">{{ roleSelection[rtype].name }}</span>
                                                    <span v-if="selected"
                                                        class="absolute inset-y-0 left-0 flex items-center pl-3 text-kashmir-600">
                                                        <PhCheck class="h-5 w-5" aria-hidden="true" />
                                                    </span>
                                                </li>
                                            </ListboxOption>
                                        </ListboxOptions>
                                    </transition>
                                </div>
                            </Listbox>
                        </td>
                        <td v-else class="px-3 py-3.5 text-left text-sm  text-gray-900">
                            {{ t(`group.roles.${member.responsibility.toLowerCase()}`) }}
                        </td>
                        <td v-if="member.researcher.email === authStore.email"
                            class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
                            <PhCheckCircle class="text-kashmir-700 h-5 w-5" aria-hidden="true" />
                        </td>
                        <td v-if="member.researcher.email !== authStore.email && groupStore.isCustodian"
                            class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
                            <button @click.prevent="removeMember(member.id)"
                                class="relative inline-flex items-center rounded-full p-2 text-xs hover:bg-cerise-50">
                                <PhTrashSimple class="md:-ml-0.5 h-4 w-4 text-cerise-400" aria-hidden="true" />
                                <span class="sr-only">
                                    {{ t("group.members.remove") }}
                                </span>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <CommonPagination />
    </div>
</template>

<script setup lang="ts">
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, } from "@headlessui/vue"
import { PhCheckCircle, PhCaretUpDown, PhCheck, PhTrashSimple } from "@phosphor-icons/vue"
import { useGroupStore, useAuthStore } from "@/stores"
import { IFilters, IRoleType, IKeyable } from "@/interfaces"
import { readableDate } from "@/utilities"

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const groupStore = useGroupStore()
const authStore = useAuthStore()
const payload = ref<IFilters>({} as IFilters)
const props = defineProps<{
    groupId: string
}>()
const parameters = ref<string[]>([])
const roleParameters: IKeyable = {
    "CUSTODIAN": ["CUSTODIAN", "CURATOR", "RESEARCHER", "VIEWER"],
    "CURATOR": ["CURATOR", "RESEARCHER", "VIEWER"],
    "RESEARCHER": ["RESEARCHER", "VIEWER"],
    "VIEWER": [],
}
const roleSelection: IKeyable = {
    "VIEWER": { value: "VIEWER", name: t("group.roles.viewer") },
    "RESEARCHER": { value: "RESEARCHER", name: t("group.roles.researcher") },
    "CURATOR": { value: "CURATOR", name: t("group.roles.curator") },
    "CUSTODIAN": { value: "CUSTODIAN", name: t("group.roles.custodian") },
}

watch(() => [route.query], async () => {
    await getAllMembers()
})

async function getAllMembers() {
    if (route.query && route.query.page && !isNaN(+route.query.page)) payload.value = { page: +route.query.page }
    await groupStore.getMembers(props.groupId, payload.value)
}

async function updateMemberRole(roleID: string, role: IRoleType) {
    await groupStore.updateMember(props.groupId, roleID, role, payload.value)
    await getAllMembers()
}

async function removeMember(memberKey: string) {
    await groupStore.removeMember(props.groupId, memberKey, payload.value)
}

function setRoleParameters() {
    if (groupStore.memberRole) {
        parameters.value = roleParameters[groupStore.memberRole]
    }
}

onMounted(async () => {
    setRoleParameters()
    await getAllMembers()
})

onBeforeUnmount(() => {
    router.replace({ query: {} })
})
</script>