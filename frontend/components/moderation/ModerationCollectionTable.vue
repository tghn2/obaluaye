<template>
    <div class="flex-auto p-3">
        <div class="w-full">
            <table class="min-w-full divide-y divide-gray-300">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                            Title
                        </th>
                        <th scope="col"
                            class="hidden px-3 py-3.5 text-left text-sm font-semibold text-gray-900 lg:table-cell">
                            Multi</th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Edit</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200 bg-white">
                    <tr v-for="collection in collectionStore.multi" :key="collection.id">
                        <td class="hidden px-3 py-4 text-sm text-gray-500 lg:table-cell">{{ collection.title }}</td>
                        <td class="hidden px-3 py-4 text-sm lg:table-cell">
                            <ModerationCheckState :check="collection.isMulti" />
                        </td>
                        <td class="px-3 py-4 text-sm text-gray-500">
                            <LocaleLink :to="`/collection/${collection.id}`">
                                <PhPencilSimple class="h-6 w-6 shrink-0 text-kashmir-600 hover:text-kashmir-800 p-1" aria-hidden="true" />
                            </LocaleLink>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PhPencilSimple } from "@phosphor-icons/vue"
import { useCollectionStore } from "@/stores"
import { IFilters } from "@/interfaces"

const route = useRoute()
const router = useRouter()
const collectionStore = useCollectionStore()
const payload = ref<IFilters>({} as IFilters)

watch(() => [route.query], async () => {
    await getAllCollections()
})

async function getAllCollections() {
    if (route.query && route.query.page && !isNaN(+route.query.page)) payload.value = { page: +route.query.page }
    await collectionStore.getMulti(payload.value)
}

onMounted(async () => {
    await getAllCollections()
})

onBeforeUnmount(() => {
    router.replace({ query: {} })
})
</script>