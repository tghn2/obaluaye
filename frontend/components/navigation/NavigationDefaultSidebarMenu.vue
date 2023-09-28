<template>
    <div class="hidden md:fixed md:inset-y-0 md:z-30 md:flex md:flex-col md:w-24 lg:w-60">
        <div class="flex grow flex-col gap-y-5 px-6">
            <div class="flex h-16 shrink-0 items-center">
                <PhStethoscope class="block h-8 w-auto lg:hidden text-spring-600" alt="Obaluaye.com" aria-hidden="true" />
                <PhStethoscope class="hidden h-8 w-auto lg:block text-spring-600" alt="Obaluaye.com" aria-hidden="true" />
            </div>
            <nav class="flex flex-1 flex-col">
                <ul role="list" class="flex flex-1 flex-col gap-y-7">
                    <!-- <li class="block lg:hidden -mx-2 space-y-1">
                        <LocaleLink to="#"
                        class="text-gray-400 hover:text-spring-600 hover:bg-gray-50 group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold">
                        <PhMagnifyingGlass class="h-6 w-6 shrink-0" aria-hidden="true" />
                        </LocaleLink>
                    </li> -->
                    <li>
                        <ul role="list" class="-mx-2 space-y-1">
                            <li v-for="item in leadNavigation" :key="item.name">
                                <LocaleLink :to="item.to" :class="[!(authStore.loggedIn || !item.login)
                                    ? 'pointer-events-none text-gray-500'
                                    : item.name === settingsStore.current.pageName
                                        ? 'bg-gray-50 text-spring-600'
                                        : 'text-gray-700 hover:text-spring-600 hover:bg-gray-50',
                                    'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                                    :disabled="!(authStore.loggedIn || !item.login)">
                                    <component :is="item.icon"
                                        :class="[item.name === settingsStore.current.pageName ? 'text-spring-600' : 'text-gray-400 group-hover:text-spring-600', 'h-6 w-6 shrink-0']"
                                        aria-hidden="true" />
                                    <span class="hidden lg:block">{{ t(item.name) }}</span>
                                </LocaleLink>
                            </li>
                        </ul>
                    </li>
                    <li>
                        <ul role="list" class="-mx-2 mt-2 space-y-1">
                            <li v-for="item in secondaryNavigation" :key="item.name">
                                <LocaleLink :to="item.to" :class="[!(authStore.loggedIn || !item.login)
                                    ? 'pointer-events-none text-gray-500'
                                    : item.name === settingsStore.current.pageName
                                        ? 'bg-gray-50 text-spring-600'
                                        : 'text-gray-700 hover:text-spring-600 hover:bg-gray-50',
                                    'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                                    :disabled="!(authStore.loggedIn || !item.login)">
                                    <component :is="item.icon"
                                        :class="[item.name === settingsStore.current.pageName ? 'text-spring-600' : 'text-gray-400 group-hover:text-spring-600', 'h-6 w-6 shrink-0']"
                                        aria-hidden="true" />
                                    <span class="hidden lg:block">{{ t(item.name) }}</span>
                                </LocaleLink>
                            </li>
                        </ul>
                    </li>
                    <li>
                        <LocaleDropdown />
                    </li>
                    <li>
                        <PwaBadge />
                        <PwaInstallPrompt />
                    </li>
                    <li class="-mx-6 mt-auto">
                        <AuthenticationSidebarNavigation />
                    </li>
                </ul>
            </nav>
        </div>
    </div>
</template>

<script setup lang="ts">
import {
    PhStethoscope,
    PhHouseSimple,
    PhGear,
    PhChatTeardropText,
    PhUsersThree,
    PhMagnifyingGlass,
    PhPath,
} from "@phosphor-icons/vue"
import { useSettingStore, useAuthStore } from "@/stores"

const settingsStore = useSettingStore()
const authStore = useAuthStore()
const { t } = useI18n()

const leadNavigation = [
    { name: "nav.home", to: "/", icon: PhHouseSimple, login: false },
    { name: "nav.pathways", to: "/pathway", icon: PhPath, login: false },
]

const secondaryNavigation = [
    // { name: "nav.comments", to: "/journey", icon: PhChatTeardropText, login: true },
    // { name: "nav.groups", to: "/projects", icon: PhUsersThree, login: true },
    { name: "nav.settings", to: "/settings", icon: PhGear, login: true },
]
</script>