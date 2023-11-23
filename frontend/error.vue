<template>
  <main class="min-h-screen">
    <div class="max-w-3xl mx-auto px-4 py-10 text-center sm:px-6 sm:py-16 lg:px-8 lg:py-20">
      <p v-show="props.error?.statusCode === 404" class="text-sm font-semibold text-kashmir-500 uppercase tracking-wide">
        {{ t("errorpage.error")}}
      </p>
      <div class="flex mt-10">
          <p class="mt-4 text-3xl font-medium text-kashmir-500">
            {{ t("errorpage.description")}}
          </p>
          <img class="h-28 sm:h-32 w-auto ml-4" src="/img/full-logo.svg" :alt="t('common.title')" />
      </div>
      <div class="mt-12">
        <button @click="handleError"
          class="mx-auto flex justify-center rounded-md border border-transparent bg-kashmir-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-kashmir-700 focus:outline-none focus:ring-2 focus:ring-kashmir-600 focus:ring-offset-2">
          {{ t("errorpage.gohome")}}
        </button>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
const { t } = useI18n()
const props = defineProps({
  error: Object
})
const handleError = () => clearError({ redirect: "/" })
</script>
