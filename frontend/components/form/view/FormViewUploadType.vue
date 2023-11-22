<template>
    <div>
        <p class="text-sm font-medium text-gray-900 mb-2">{{ t("form.types.upload") }}</p>
        <div class="group flex items-center gap-x-3 text-sm leading-6 sm:px-1">
            <PhUploadSimple class="text-gray-400 h-5 w-5 shrink-0" aria-hidden="true" />
            <span class="text-sm text-gray-900">{{ t("form.uploadText") }}</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhCircle, PhUploadSimple } from "@phosphor-icons/vue"
import { IForm, IResponse } from "@/interfaces"

const { t } = useI18n()

const props = defineProps<{
    form: IForm,
    response: IResponse,
}>()
</script>