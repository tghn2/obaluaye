<template>
    <main class="max-w-none mx-auto prose prose-reader-light prose-reader-base prose-reader-compact pt-10 pb-20">
        <!-- @vue-ignore -->
        <ContentDoc :query="{ path: pathWithoutLocale, where: { _locale: locale } }" />
    </main>
</template>

<script setup lang="ts">
const { locale } = useI18n()
const { path } = useRoute()
// https://stackblitz.com/edit/nuxt-starter-jnysug?file=pages%2F[...slug].vue
const pathWithoutLocale = path.replace(
  new RegExp(`^/${locale.value}(\/|$)`),
  "/"
)
const { data, error } = await useAsyncData(`content-${path}`, () => {
  return queryContent().where({ _path: path }).findOne();
})
if (error.value) {
  throw createError({ statusCode: 404, statusMessage: "Page Not Found" })
}

</script>
  