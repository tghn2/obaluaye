<template>
    <div class="hidden md:fixed md:inset-y-0 md:z-30 md:flex md:flex-col md:w-24 lg:w-60">
        <div class="flex grow flex-col gap-y-5 px-6">
            <div class="flex h-16 shrink-0 items-center">
                <PhStethoscope class="block h-8 w-auto lg:hidden text-kashmir-600" alt="Obaluaye.com" aria-hidden="true" />
                <PhStethoscope class="hidden h-8 w-auto lg:block text-kashmir-600" alt="Obaluaye.com" aria-hidden="true" />
            </div>
            <nav class="flex flex-1 flex-col">
                <ul role="list" class="flex flex-1 flex-col gap-y-7">
                    <!-- <li class="block lg:hidden -mx-2 space-y-1">
                        <LocaleLink to="#"
                        class="text-gray-400 hover:text-kashmir-600 hover:bg-gray-50 group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold">
                        <PhMagnifyingGlass class="h-6 w-6 shrink-0" aria-hidden="true" />
                        </LocaleLink>
                    </li> -->
                    <li>
                        <ul role="list" class="-mx-2 space-y-1">
                            <li v-for="item in leadNavigation" :key="item.name">
                                <LocaleLink :to="item.to" :class="[!(authStore.loggedIn || !item.login)
                                    ? 'pointer-events-none text-gray-500'
                                    : item.name === settingsStore.current.pageName
                                        ? 'bg-gray-50 text-kashmir-600'
                                        : 'text-gray-700 hover:text-kashmir-600 hover:bg-gray-50',
                                    'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                                    :disabled="!(authStore.loggedIn || !item.login)">
                                    <component :is="item.icon"
                                        :class="[item.name === settingsStore.current.pageName ? 'text-kashmir-600' : 'text-gray-400 group-hover:text-kashmir-600', 'h-6 w-6 shrink-0']"
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
                                        ? 'bg-gray-50 text-kashmir-600'
                                        : 'text-gray-700 hover:text-kashmir-600 hover:bg-gray-50',
                                    'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                                    :disabled="!(authStore.loggedIn || !item.login)">
                                    <component :is="item.icon"
                                        :class="[item.name === settingsStore.current.pageName ? 'text-kashmir-600' : 'text-gray-400 group-hover:text-kashmir-600', 'h-6 w-6 shrink-0']"
                                        aria-hidden="true" />
                                    <span class="hidden lg:block">{{ t(item.name) }}</span>
                                    <span v-if="item.showDot" class="relative">
                                        <svg viewBox="0 0 100 100" class="absolute -ml-5 z-10 h-[2rem] w-[2rem]"
                                            aria-hidden="true">
                                            <circle cx="50" cy="20" r="10" fill="#d93e8a" />
                                        </svg>
                                    </span>
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
    PhDot,
} from "@phosphor-icons/vue"
import { useSettingStore, useAuthStore } from "@/stores"

const settingsStore = useSettingStore()
const authStore = useAuthStore()
const { t } = useI18n()

const leadNavigation = [
    { name: "nav.home", to: "/", icon: PhHouseSimple, login: false, showDot: false },
    { name: "nav.comments", to: "/comment", icon: PhChatTeardropText, login: true, showDot: false },
    { name: "nav.groups", to: "/group", icon: PhUsersThree, login: true, showDot: false },
]

const secondaryNavigation = [
    { name: "nav.pathways", to: "/pathway", icon: PhPath, login: false, showDot: false },
    { name: "nav.settings", to: "/settings", icon: PhGear, login: true, showDot: authStore.profile.invitationCount > 0 },
]
</script>