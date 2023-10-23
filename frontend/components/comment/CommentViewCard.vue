<template>
    <div class="flex-auto rounded-md p-3 ring-1 ring-inset ring-gray-200">
        <div class="flex justify-between gap-x-4">
            <div class="py-0.5 text-xs leading-5 text-gray-500">
                <span v-if="props.comment.researcher && props.comment.researcher.full_name"
                    class="font-medium text-gray-900">
                    {{ props.comment.researcher.full_name }}
                </span>
                <span
                    v-if="props.comment.researcher && !props.comment.researcher.full_name && props.comment.researcher.email"
                    class="font-medium text-gray-900">
                    {{ props.comment.researcher.email }}
                </span>
            </div>
            <time :datetime="props.comment.modified" class="flex-none py-0.5 text-xs leading-5 text-gray-500">
                {{ readableDate(props.comment.modified as string, true, settingStore.locale) }}
            </time>
        </div>
        <p v-if="!editPost" class="text-sm leading-6 text-gray-500">{{ draft.content }}</p>
        <form v-else class="relative flex-auto">
            <div
                class="overflow-hidden rounded-lg pb-12 shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-kashmir-600">
                <label for="comment" class="sr-only">{{ t("comment.placeholder") }}</label>
                <textarea rows="2" name="comment" id="comment" v-model="draft.content"
                    class="block w-full resize-none border-0 bg-transparent py-1.5 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                    :placeholder="`${t('comment.placeholder')}...`" />
            </div>
            <div class="absolute inset-x-0 bottom-0 flex justify-end space-x-4 py-2 pl-3 pr-2">
                <button type="button" @click="toggleEdit">
                    <PhPencilSimpleSlash
                        class="h-8 w-8 shrink-0 bg-cerise-400 hover:bg-cerise-600 text-white rounded-lg p-1"
                        aria-hidden="true" />
                </button>
                <button v-if="editPost" type="button" @click="updatePost">
                    <PhPaperPlaneRight
                        class="h-8 w-8 shrink-0 bg-kashmir-400 hover:bg-kashmir-600 text-white rounded-lg p-1"
                        aria-hidden="true" />
                </button>
            </div>
        </form>
        <div class="absolute inset-x-0 bottom-0 flex justify-end py-2 pl-3 pr-2">
            <button v-if="!editPost && authStore.profile.id === draft.researcher_id" type="button" @click="toggleEdit">
                <PhPencilSimple class="h-6 w-6 shrink-0 bg-kashmir-400 hover:bg-kashmir-600 text-white rounded-full p-1"
                    aria-hidden="true" />
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPencilSimple, PhPencilSimpleSlash, PhPaperPlaneRight } from "@phosphor-icons/vue"
import { IComment } from "@/interfaces"
import { useAuthStore, useSettingStore, useTokenStore } from "@/stores"
import { readableDate } from "@/utilities"
import { apiComment } from "@/api"

const { t } = useI18n()
const settingStore = useSettingStore()
const authStore = useAuthStore()
const tokenStore = useTokenStore()
const editPost = ref(false)
const draft = ref<IComment>({ content: "" })
const props = defineProps<{
    comment: IComment,
}>()
const emit = defineEmits<{ setResponse: [response: boolean] }>()

// SETTERS
async function updatePost() {
    await tokenStore.refreshTokens()
    if (tokenStore.token && authStore.profile.id === draft.value.researcher_id) {
        try {
            const { data: response } = await apiComment.updateTerm(tokenStore.token, draft.value.id as string, { ...draft.value })
            if (response.value) emit("setResponse", true)
        } catch (error) { }
    }
    editPost.value = false
}

async function toggleResolved() {
    await tokenStore.refreshTokens()
    if (tokenStore.token) {
        try {
            const { data: response } = await apiComment.resolveTerm(tokenStore.token, draft.value.id as string)
            if (response.value) emit("setResponse", true)
        } catch (error) { }
    }
}

function toggleEdit() {
    if (editPost.value) resetDraft()
    editPost.value = !editPost.value
}

// GETTERS
function resetDraft() {
    draft.value = { ...props.comment }
}

onMounted(async () => {
    resetDraft()
})
</script>