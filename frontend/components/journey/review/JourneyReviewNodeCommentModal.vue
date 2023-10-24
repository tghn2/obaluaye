<template>
    <div>
        <div class="flex justify-end">
            <button type="button" @click="openModal"
                class="text-xs font-medium leading-6 text-white bg-kashmir-700 mx-3 px-2 py-0.5 rounded-b-lg">
                <div class="flex flex-inline items-center space-x-2">
                    <span>{{ currentCount }}</span>
                    <PhChatTeardropText class="h-6 w-6 shrink-0" aria-hidden="true" />
                </div>
            </button>
        </div>
        <TransitionRoot appear :show="isOpen" as="template">
            <Dialog as="div" @close="closeModal" class="relative z-30">
                <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100"
                    leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
                    <div class="fixed inset-0 bg-black bg-opacity-25" />
                </TransitionChild>
                <div class="fixed inset-0 overflow-y-auto">
                    <div class="flex min-h-full max-w-3xl mx-auto items-center justify-center">
                        <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95"
                            enter-to="opacity-100 scale-100" leave="duration-200 ease-in" leave-from="opacity-100 scale-100"
                            leave-to="opacity-0 scale-95">
                            <DialogPanel
                                class="w-full max-w-md transform overflow-hidden rounded-md bg-white p-6 text-left align-middle shadow-xl transition-all">
                                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                                    {{ t("comment.name") }}
                                </DialogTitle>
                                <div class="flex-auto mt-2">
                                    <CommentPostCard :comment="draftPost" @set-response="watchCreatePost" />
                                    <ul role="list" class="space-y-3 mt-3">
                                        <li v-for="comment in comments" :key="comment.id" class="relative flex gap-x-4">
                                            <CommentViewCard :comment="comment" @set-response="watchUpdatePost" />
                                        </li>
                                    </ul>
                                </div>
                                <div class="flex flex-inline items-center space-x-2 justify-end mt-4">
                                    <button type="button" @click="closeModal"
                                        class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-md px-3 py-2 text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                                        <PhX class="md:-ml-0.5 h-4 w-4 text-gray-400" aria-hidden="true" />
                                        <span class="hidden md:block">{{ t("comment.close") }}</span>
                                    </button>
                                </div>
                            </DialogPanel>
                        </TransitionChild>
                    </div>
                </div>
            </Dialog>
        </TransitionRoot>
    </div>
</template>
  
<script setup lang="ts">
import { PhX, PhChatTeardropText } from "@phosphor-icons/vue"
import {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
    DialogTitle,
} from "@headlessui/vue"
import { useAuthStore, useTokenStore } from "@/stores"
import { IComment } from "@/interfaces"
import { apiComment } from "@/api"

const { t } = useI18n()
const isOpen = ref(false)
const authStore = useAuthStore()
const tokenStore = useTokenStore()
const draftPost = ref<IComment>({})
const comments = ref<IComment[]>([])
const currentCount = ref(0)
const props = defineProps<{
    responseId: string,
    commentCount: number,
}>()

// WATCHERS
async function watchCreatePost(payload: IComment) {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
        try {
            comments.value = []
            const { data: response } = await apiComment.createTerm(tokenStore.token, props.responseId, payload)
            if (response.value) await getResponseComments()
        } catch (error) { }
    }
    resetComments()
}

async function watchUpdatePost(payload: boolean) {
    if (payload) await getResponseComments()
}

// SETTERS
function updateComments(response: IComment[]) {
    comments.value = [...response]
    currentCount.value = comments.value.length
}

// GETTERS
async function getResponseComments() {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
        try {
            comments.value = []
            const { data: response } = await apiComment.getTerm(tokenStore.token, props.responseId)
            if (response.value) updateComments(response.value)
        } catch (error) { }
    }
}

function resetComments() {
    draftPost.value = {
        response_id: props.responseId,
        researcher_id: authStore.profile.id,
        content: "",
    }
}

onMounted(async () => {
    resetComments()
    if (props.commentCount) currentCount.value = props.commentCount
    await getResponseComments()
})

// MODAL
function closeModal() {
    isOpen.value = false
}
function openModal() {
    isOpen.value = true
}
</script>
  