<template>
    <div class="flex-auto p-3">
        <div class="shadow sm:overflow-hidden sm:rounded-md min-w-max">
            <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Invited</th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Email</th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Response</th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">By</th>
                        <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                    <tr v-for="invite in groupStore.invitations" :key="invite.id">
                        <td class="px-3 py-3.5 text-left text-sm text-gray-900">
                            <time :datetime="invite.created">{{ readableDate(invite.created as string) }}</time>
                        </td>
                        <td class="px-3 py-3.5 text-left text-sm text-gray-900">
                            {{ invite.email }}
                        </td>
                        <td class="px-3 py-3.5 text-left text-sm  text-gray-900">{{ invite.response }}</td>
                        <td class="px-3 py-3.5 text-left text-sm text-gray-900">{{ invite.sender.email }}</td>
                        <td class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
                            <button @click.prevent="removeInvitation(invite.id)"
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
import { PhTrashSimple } from "@phosphor-icons/vue"
import { useGroupStore } from "@/stores"
import { IFilters } from "@/interfaces"
import { readableDate } from "@/utilities"

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const groupStore = useGroupStore()
const payload = ref<IFilters>({} as IFilters)
const props = defineProps<{
    groupId: string
}>()

watch(() => [route.query], async () => {
    await getAllInvitations()
})

function setPage() {
    if (route.query && route.query.page && !isNaN(+route.query.page)) payload.value = { page: +route.query.page }
}

async function removeInvitation(inviteKey: string) {
    setPage()
    await groupStore.removeInvitation(props.groupId, inviteKey, payload.value)
}

async function getAllInvitations() {
    setPage()
    await groupStore.getInvitations(props.groupId, payload.value)
}

onMounted(async () => {
    await getAllInvitations()
})

onBeforeUnmount(() => {
    router.replace({ query: {} })
})
</script>