<template>
    <div class="min-w-full hover:bg-gray-100">
        <LocaleLink :to="`/pathway/${props.pathway.id}`">
            <div class="flex w-full items-center">
                <div class="flex-1">
                    <div class="flex justify-between gap-x-4">
                        <div class="py-0.5 text-sm leading-6 text-gray-500">
                            <h2 class="font-bold text-gray-900">{{ props.pathway.title }}</h2>
                        </div>
                        <ul role="list" class="flex flex-row justify-end text-xs py-0.5">
                            <li
                                :class="[!authStore.completedPathway && props.pathway.pathType === 'PERSONAL' ? 'bg-cerise-100 rounded-md text-gray-700' : 'text-gray-500', 'relative group flex flex-row items-center leading-6 text-xs font-medium gap-x-1 px-1']">
                                <PhFlask v-if="props.pathway.pathType === 'RESEARCH'" class="text-gray-700 h-4 w-4 shrink-0"
                                    aria-hidden="true" />
                                <PhUser v-else class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                                {{ pathTypeText[props.pathway.pathType].toUpperCase() }}
                            </li>
                            <li v-if="props.pathway.isFeatured"
                                class="relative group flex flex-row text-xs font-medium text-gray-500 gap-x-1 pl-2">
                                <PhFeather class="text-yellow-600 h-4 w-4 shrink-0" aria-hidden="true" />
                            </li>
                            <li v-if="props.pathway.isPrivate"
                                class="relative group flex flex-row text-xs font-medium text-gray-500 gap-x-1 pl-2">
                                <PhEyeSlash class="text-cerise-700 h-4 w-4 shrink-0" aria-hidden="true" />
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <p v-if="props.pathway.description" class="text-sm leading-5 text-gray-500">{{ props.pathway.description }}</p>
            <div class="flex items-center justify-between mt-2">
                <div class="group flex flex-row text-xs font-medium text-gray-700">
                    <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span v-if="props.pathway.subjects && props.pathway.subjects.length" class="ml-1">
                        {{ props.pathway.subjects.join(", ") }}
                    </span>
                    <span v-else class="ml-1">
                        {{ t("multi.untagged") }}
                    </span>
                </div>
            </div>
        </LocaleLink>
    </div>
</template>

<script setup lang="ts">
import { PhFlask, PhUser, PhTag, PhEyeSlash, PhFeather } from "@phosphor-icons/vue"
import { IPathway } from "@/interfaces"
import { useAuthStore } from "@/stores"

const props = defineProps<{
    pathway: IPathway
}>()
const { t } = useI18n()
const authStore = useAuthStore()
const pathTypeText = {
    PERSONAL: t("pathway.types.personal"),
    RESEARCH: t("pathway.types.research"),
}
</script>