<template>
    <div class="mt-6 flex gap-x-3">
        <PhChatTeardropText class="h-7 w-7 shrink-0 bg-spring-400 text-white rounded-full p-1" aria-hidden="true" />
        <form class="relative flex-auto">
            <div
                class="overflow-hidden rounded-lg pb-12 shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-kashmir-600">
                <label for="comment" class="sr-only">{{ t("comment.placeholder") }}</label>
                <textarea rows="2" name="comment" id="comment" v-model="draft.content"
                    class="block w-full resize-none border-0 bg-transparent py-1.5 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6"
                    :placeholder="`${t('comment.placeholder')}...`" />
            </div>
            <div class="absolute inset-x-0 bottom-0 flex justify-end py-2 pl-3 pr-2">
                <button type="button" @click="postComment">
                    <PhPaperPlaneRight
                        class="h-8 w-8 shrink-0 bg-kashmir-400 hover:bg-kashmir-600 text-white rounded-lg p-1"
                        aria-hidden="true" />
                </button>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { PhChatTeardropText, PhPaperPlaneRight } from "@phosphor-icons/vue"
import { IComment } from "@/interfaces"

const { t } = useI18n()
const draft = ref({} as IComment)
const props = defineProps<{
    comment: IComment,
}>()
const emit = defineEmits<{ setResponse: [draft: IComment] }>()

function postComment() {
    emit("setResponse", { ...draft.value })
    draft.value.content = props.comment.content
}

onMounted(async () => {
    draft.value = { ...props.comment }
})
</script>