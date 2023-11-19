<template>
    <main class="max-w-none mx-auto prose prose-reader-light prose-reader-base prose-reader-compact pt-10 pb-20">
        <!-- @vue-ignore -->
        <ContentDoc :query="{ path: pathWithoutLocale, where: { _locale: locale } }" />
    </main>
</template>

<script setup lang="ts">
const { locale } = useI18n()
const route = useRoute()
// https://stackblitz.com/edit/nuxt-starter-jnysug?file=pages%2F[...slug].vue
const pathWithoutLocale = route.path.replace(
  new RegExp(`^/${locale.value}(\/|$)`),
  "/"
)

</script>
  