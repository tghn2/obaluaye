<template>
    <div class="min-w-full hover:bg-gray-100">
        <LocaleLink :to="`/group/${props.group.id}`">
            <div class="flex w-full items-center">
                <div class="flex-1">
                    <div class="flex justify-between gap-x-4">
                        <div class="py-0.5 text-sm leading-5 text-gray-500">
                            <h2 class="font-bold text-gray-900">{{ props.group.title }}</h2>
                        </div>
                        <ul role="list" class="flex flex-row justify-end text-xs leading-5 py-0.5">
                            <li v-if="props.group && props.group.roles"
                                class="relative group flex flex-row text-xs font-medium text-gray-500 gap-x-1 pl-2">
                                <PhUsers class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                                {{ props.group.roles.length }}
                            </li>
                            <li v-if="props.group.isComplete" class="flex items-center pl-2">
                                <PhChecks class="text-spring-600 h-4 w-4 shrink-0" aria-hidden="true" />
                            </li>
                            <li v-if="props.group.isFeatured" class="flex items-center pl-2">
                                <PhFeather class="text-yellow-600 h-4 w-4 shrink-0" aria-hidden="true" />
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <p v-if="props.group.description" class="text-sm leading-6 text-gray-500">{{ props.group.description }}</p>
            <div class="flex items-center justify-between">
                <div class="group flex flex-row text-xs font-medium text-gray-700">
                    <PhTag class="text-gray-700 h-4 w-4 shrink-0" aria-hidden="true" />
                    <span v-if="props.group.subjects && props.group.subjects.length" class="ml-1">
                        {{ props.group.subjects.join(", ") }}
                    </span>
                    <span v-else class="ml-1">
                        {{ t("multi.untagged") }}
                    </span>
                </div>
                <ul role="list" class="flex flex-row justify-end text-xs">
                    <h3 id="detail-heading" class="sr-only">Pathway link</h3>
                    <li v-if="props.group.pathway && props.group.pathway.id && props.group.pathway.title" class="relative">
                        <LocaleLink :to="`/pathway/${props.group.pathway!.id}`"
                            class="text-gray-700 hover:text-kashmir-600 group flex gap-x-1 p-2 font-semibold">
                            <PhPath class="text-gray-700 group-hover:text-kashmir-600 h-4 w-4 shrink-0"
                                aria-hidden="true" />
                            <span class="hidden lg:block">{{ props.group.pathway!.title }}</span>
                        </LocaleLink>
                    </li>
                </ul>
            </div>
        </LocaleLink>
    </div>
</template>

<script setup lang="ts">
import { PhPath, PhTag, PhUsers, PhFeather, PhChecks } from "@phosphor-icons/vue"
import { IGroup } from "@/interfaces"

const { t } = useI18n()
const props = defineProps<{
    group: IGroup
}>()
</script>