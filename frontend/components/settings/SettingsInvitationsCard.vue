<template>
    <div class="w-full">
        <div>
            <div class="pt-6 px-4 sm:px-6">
                <h3 class="text-lg font-medium leading-6 text-gray-900">{{ t("settings.invitations.title") }}</h3>
                <p class="mt-1 text-sm text-gray-500">
                    {{ t("settings.invitations.description") }}
                </p>
            </div>
            <JourneyCompletePersonalPathBanner v-if="!authStore.profile.completedPersonalPathway" />
            <div class="flex-auto p-3">
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
                                <time :datetime="invite.created">
                                    {{ readableDate(invite.created as string, true, groupStore.settings.locale) }}
                                </time>
                            </td>
                            <td class="px-3 py-3.5 text-left text-sm truncate text-gray-900">
                                <span v-if="invite.group">{{ invite.group.title }}</span>
                            </td>
                            <td class="px-3 py-3.5 text-left text-sm text-gray-900">
                                <span v-if="invite.sender.full_name">{{ invite.sender.full_name }}</span>
                                <span v-else>{{ invite.sender.email }}</span>
                            </td>
                            <td class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
                                <button @click.prevent="acceptInvitation(invite.id)"
                                    class="text-spring-700 hover:text-kashmir-600 group flex gap-x-1 p-2 font-semibold"
                                    :disabled="!authStore.profile.completedPersonalPathway">
                                    <PhCheck class="text-kashmir-700 group-hover:text-kashmir-600 h-4 w-4 shrink-0"
                                        aria-hidden="true" />
                                    <span class="sr-only">
                                        {{ t("settings.invitations.accept") }}
                                    </span>
                                </button>
                            </td>
                            <td class="pl-3 py-3.5 justify-center items-center text-sm text-gray-900">
                                <button @click.prevent="rejectInvitation(invite.id)"
                                    class="text-spring-700 hover:text-kashmir-600 group flex gap-x-1 p-2 font-semibold"
                                    :disabled="!authStore.profile.completedPersonalPathway">
                                    <PhTrashSimple class="text-spring-700 group-hover:text-kashmir-600 h-4 w-4 shrink-0"
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
    </div>
</template>

<script setup lang="ts">
import { PhCheck, PhTrashSimple } from "@phosphor-icons/vue"
import { useAuthStore, useGroupStore } from "@/stores"
import { IFilters } from "@/interfaces"
import { readableDate } from "@/utilities"

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const groupStore = useGroupStore()
const payload = ref<IFilters>({} as IFilters)

watch(() => [route.query], async () => {
    await getAllInvitations()
})

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