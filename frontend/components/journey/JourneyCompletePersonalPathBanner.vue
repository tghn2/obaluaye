<template>
    <div class="sm:px-6 sm:py-2 lg:px-8">
        <div
            class="flex items-center justify-between gap-x-6 bg-cerise-800 px-6 py-2.5 sm:rounded-xl sm:py-3 sm:pl-4 sm:pr-3.5">
            <p class="text-sm leading-6 text-white">
                {{ t("settings.invitations.completePathway") }}
            </p>
            <span class="text-sm leading-6 text-white" aria-hidden="true">&rarr;</span>
            <LocaleLink to="/pathway"
                class="group flex items-center gap-x-1 text-sm leading-6 font-semibold text-white ring-1 rounded-md p-1 px-1 ring-white hover:bg-cerise-700">
                <PhPath class="h-5 w-5" aria-hidden="true" />
                <span>{{ t("nav.pathways") }}</span>
            </LocaleLink>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPath } from "@phosphor-icons/vue"

const { t } = useI18n()
</script>