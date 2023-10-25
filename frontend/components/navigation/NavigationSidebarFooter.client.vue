<template>
    <footer>
        <div class="mx-auto overflow-hidden py-8">
            <nav class="-mx-5 -my-2 flex flex-wrap justify-center" aria-label="Footer">
                <div v-for="item in footerNavigation.main" :key="item.name">
                    <LocaleLink :to="item.to" class="text-sm text-gray-400 hover:text-gray-300">
                        {{ t(item.name) }}
                    </LocaleLink>
                    <span v-show="item.dot" class="text-sm text-gray-400 px-2">&middot;</span>
                </div>
            </nav>
            <p class="mt-5 text-center text-xs text-gray-400">
                &copy; 2023 {{ t("common.title") }}. {{ t("footer.rights") }}
            </p>
        </div>
    </footer>
</template>

<script setup lang="ts">
const { t } = useI18n()

const footerNavigation = {
    main: [
        { name: "nav.about", to: "/about", dot: true },
        { name: "nav.privacy", to: "/privacy", dot: true },
        { name: "nav.contact", to: "/contact", dot: false },
    ],
}
</script>