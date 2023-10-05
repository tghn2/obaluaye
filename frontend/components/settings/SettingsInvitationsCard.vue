<template>
    <div class="flex-auto p-3">
        <div class="w-full">
            <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                            {{ t("settings.invitations.invited") }}
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                            {{ t("settings.invitations.for") }}
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                            {{ t("settings.invitations.by") }}
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
                        <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900"></th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                    <tr v-for="invite in groupStore.invitations" :key="invite.id">
                        <td class="px-3 py-3.5 text-left text-sm text-gray-900">
                            <time :datetime="invite.created">{{ readableDate(invite.created as string) }}</time>
                        </td>
                        <td class="px-3 py-3.5 text-left text-sm truncate text-gray-900">{{ getGroupName(invite.group)
                        }}</td>
                        <td class="px-3 py-3.5 text-left text-sm text-gray-900">{{ invite.sender.email }}</td>
                        <td class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
                            <button @click.prevent="acceptInvitation(invite.id)"
                                class="text-cyan-700 hover:text-spring-600 group flex gap-x-1 p-2 font-semibold">
                                <PhCheck class="text-spring-700 group-hover:text-spring-600 h-4 w-4 shrink-0"
                                    aria-hidden="true" />
                                <span class="sr-only">
                                    {{ t("settings.invitations.accept") }}
                                </span>
                            </button>
                        </td>
                        <td class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
                            <button @click.prevent="rejectInvitation(invite.id)"
                                class="text-cyan-700 hover:text-spring-600 group flex gap-x-1 p-2 font-semibold">
                                <PhTrashSimple class="text-cyan-700 group-hover:text-spring-600 h-4 w-4 shrink-0"
                                    aria-hidden="true" />
                                <span class="sr-only">
                                    {{ t("settings.invitations.reject") }}
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
import { PhCheck, PhTrashSimple } from "@phosphor-icons/vue"
import { useGroupStore } from "@/stores"
import { IFilters, IModelSummary } from "@/interfaces"
import { readableDate } from "@/utilities"

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const groupStore = useGroupStore()
const payload = ref<IFilters>({} as IFilters)

watch(() => [route.query], async () => {
    await getAllInvitations()
})

function getGroupName(group: IModelSummary) {
    if (group.title) return group.title
    return group.name
}

function setPage() {
    if (route.query && route.query.page && !isNaN(+route.query.page)) payload.value = { page: +route.query.page }
}

async function rejectInvitation(inviteKey: string) {
    setPage()
    await groupStore.rejectInvitation(inviteKey, payload.value)
}

async function acceptInvitation(inviteKey: string) {
    setPage()
    await groupStore.acceptInvitation(inviteKey, payload.value)
}

async function getAllInvitations() {
    setPage()
    await groupStore.getMembershipInvitations(payload.value)
}

onMounted(async () => {
    await getAllInvitations()
})

onBeforeUnmount(() => {
    router.replace({ query: {} })
})
</script>