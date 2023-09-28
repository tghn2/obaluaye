<template>
    <Html :lang="htmlAttrs.lang" :dir="htmlAttrs.dir">

    <Body>
        <div class="flex flex-col">
            <div class="mx-auto w-full max-w-5xl grow lg:flex">
                <slot name="header">
                    <!-- Responsive menus -->
                    <NavigationDefaultSidebarMenu />
                    <NavigationDefaultMobileMenu />
                </slot>
                <main class="mt-10 md:mt-0 md:pl-20 lg:pl-60">
                    <div class="min-h-full flex-grow">
                        <slot />
                    </div>
                    <slot name="sidebar">
                        <NavigationSidebarFooter />
                    </slot>
                </main>
                <slot name="notifications">
                    <CommonNotification />
                </slot>
            </div>
        </div>
    </Body>

    </Html>
</template>

<script setup lang="ts">
const head = useLocaleHead({
    addDirAttribute: true,
    addSeoAttributes: true,
})
const htmlAttrs = computed(() => head.value.htmlAttrs!)
</script>