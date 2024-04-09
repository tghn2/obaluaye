<template>
    <div>
        <!-- TOP BAR -->
        <div class="fixed top-0 z-30 w-full flex items-center gap-x-6 bg-white/90 px-4 py-4 sm:px-6 md:hidden">
            <div v-if="headingTerm && Object.keys(headingTerm).length !== 0"
                class="group inline-flex gap-x-3 flex-1 text-md font-semibold leading-6 text-kashmir-600">
                <component :is="headingTerm.icon" class="text-kashmir-600 h-6 w-6 shrink-0" aria-hidden="true" />
                {{ t(headingTerm.name) }}
            </div>
            <div v-else class="group inline-flex gap-x-3 flex-1 text-md font-semibold leading-6 text-kashmir-600">
                {{ t(settingsStore.current.pageName) }}
            </div>
            <AuthenticationNavigation />
        </div>
        <!-- BOTTOM BAR -->
        <Popover as="div" class="z-30 fixed md:hidden inset-x-0 bottom-0 w-full bg-white">
            <div class="max-w-full mx-auto">
                <nav class="relative grid grid-cols-4 gap-4 justify-center py-1" aria-label="Global">
                    <div v-for="(item, i) in baseNavigation">
                        <LocaleLink
                            v-if="(authStore.loggedIn || !item.login)"
                            :key="`basenav-${i}`" :to="item.to" 
                            :class="[!(authStore.loggedIn || !item.login)
                            ? 'pointer-events-none text-gray-500'
                            : item.name === settingsStore.current.pageName
                                ? 'bg-gray-50 text-kashmir-600'
                                : 'text-gray-700 hover:text-kashmir-600 hover:bg-gray-50',
                            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold justify-center']"
                            :disabled="!(authStore.loggedIn || !item.login)">
                            <component :is="item.icon"
                                :class="[item.name === settingsStore.current.pageName ? 'text-kashmir-600' : 'text-gray-400 group-hover:text-kashmir-600', 'h-6 w-6 shrink-0 inline-flex items-center']"
                                aria-hidden="true" />
                        </LocaleLink>
                    </div>
                    <PopoverButton
                        class="group flex-col inline-flex items-center gap-x-3 rounded-md p-2 text-sm font-semibold">
                        <span class="sr-only">Open user menu</span>
                        <PhDotsThreeOutline class="block h-6 w-6 text-kashmir-500" />
                    </PopoverButton>
                </nav>
            </div>
            <transition enter-active-class="transition ease-out duration-200"
                enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95">
                <PopoverPanel
                    class="-top-4 transform -translate-y-full absolute z-10 mt-2 w-full origin-top-right rounded-md bg-white/90 pt-1 shadow-md ring-1 ring-black ring-opacity-5 focus:outline-none overflow-x-visible">
                    <div v-for="(item, i) in leadNavigation">
                        <LocaleLink
                            v-if="(authStore.loggedIn || !item.login)"
                            :key="`scndrynav-${i}`" :to="item.to" :class="[!(authStore.loggedIn || !item.login)
                            ? 'pointer-events-none text-gray-500'
                            : item.name === settingsStore.current.pageName
                                ? 'bg-gray-50 text-kashmir-600'
                                : 'text-gray-700 hover:text-kashmir-600 hover:bg-gray-50',
                            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                            :disabled="!(authStore.loggedIn || !item.login)">
                            <component :is="item.icon"
                                :class="[item.name === settingsStore.current.pageName ? 'text-kashmir-600' : 'text-gray-400 group-hover:text-kashmir-600', 'h-6 w-6 shrink-0']"
                                aria-hidden="true" />
                            {{ t(item.name) }}
                        </LocaleLink>
                    </div>
                    <div v-for="(item, i) in secondaryNavigation">
                        <LocaleLink
                            v-if="(authStore.loggedIn || !item.login)"
                            :key="`scndrynav-${i}`" :to="item.to" :class="[!(authStore.loggedIn || !item.login)
                            ? 'pointer-events-none text-gray-500'
                            : item.name === settingsStore.current.pageName
                                ? 'bg-gray-50 text-kashmir-600'
                                : 'text-gray-700 hover:text-kashmir-600 hover:bg-gray-50',
                            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']"
                            :disabled="!(authStore.loggedIn || !item.login)">
                            <component :is="item.icon"
                                :class="[item.name === settingsStore.current.pageName ? 'text-kashmir-600' : 'text-gray-400 group-hover:text-kashmir-600', 'h-6 w-6 shrink-0']"
                                aria-hidden="true" />
                            {{ t(item.name) }}
                            <span v-if="item.showDot" class="relative">
                                <svg viewBox="0 0 100 100" class="absolute -ml-5 z-10 h-[2rem] w-[2rem]" aria-hidden="true">
                                    <circle cx="50" cy="20" r="10" fill="#d93e8a" />
                                </svg>
                            </span>
                        </LocaleLink>
                    </div>
                    <div v-if="authStore.loggedIn && authStore.isAdmin">
                        <LocaleLink 
                            to="/moderation" 
                            :class="['nav.moderation' === settingsStore.current.pageName
                                ? 'bg-gray-50 text-kashmir-600'
                                : 'text-gray-700 hover:text-kashmir-600 hover:bg-gray-50',
                            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                            <PhGear
                                :class="['nav.moderation' === settingsStore.current.pageName
                                    ? 'text-kashmir-600'
                                    : 'text-gray-400 group-hover:text-kashmir-600',
                                    'h-6 w-6 shrink-0']"
                                aria-hidden="true" />
                            {{ t('nav.moderation') }}
                        </LocaleLink>
                    </div>
                    <div class="p-2">
                        <LocaleDropdown />
                    </div>
                    <div>
                        <PwaBadge />
                        <PwaInstallPrompt />
                    </div>
                    <div class="flex flex-wrap justify-center bg-gray-50 mt-2 py-3">
                        <div v-for="item in footerNavigation" :key="item.name">
                            <LocaleLink :to="item.to" class="text-sm text-gray-400 hover:text-gray-300">{{ t(item.name) }}
                            </LocaleLink>
                            <span v-show="item.dot" class="text-sm text-gray-400 px-2">&middot;</span>
                        </div>
                    </div>
                </PopoverPanel>
            </transition>
        </Popover>
    </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia"
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue"
import {
    PhHouseSimple,
    PhUserGear,
    PhChatTeardropText,
    PhUsersThree,
    PhMagnifyingGlass,
    PhPath,
    PhDotsThreeOutline,
    PhGear,
} from "@phosphor-icons/vue"
import { useSettingStore, useAuthStore } from "@/stores"

const settingsStore = useSettingStore()
const { pageName } = storeToRefs(settingsStore)
const authStore = useAuthStore()
const headingTerm = shallowRef({} as INav)
const { t } = useI18n()

interface INav {
    name: string
    to: string
    icon: any
    login: boolean
    showDot: boolean
}

watch(() => pageName.value, () => {
    headingTerm.value = getCurrent()
})

const baseNavigation: INav[] = [
    { name: "nav.home", to: "/", icon: PhHouseSimple, login: false, showDot: false },
    { name: "nav.search", to: "/search", icon: PhMagnifyingGlass, login: false, showDot: false },
    { name: "nav.groups", to: "/group", icon: PhUsersThree, login: true, showDot: false },
]
const leadNavigation: INav[] = [
    { name: "nav.home", to: "/", icon: PhHouseSimple, login: false, showDot: false },
    { name: "nav.groups", to: "/group", icon: PhUsersThree, login: true, showDot: false },
]
const secondaryNavigation: INav[] = [
    { name: "nav.pathways", to: "/pathway", icon: PhPath, login: false, showDot: false },
    { name: "nav.comments", to: "/comment", icon: PhChatTeardropText, login: true, showDot: false },
    { name: "nav.settings", to: "/settings", icon: PhUserGear, login: true, showDot: authStore.profile.invitationCount > 0 },
]
const footerNavigation = [
    { name: "nav.about", to: "/about", dot: true },
    { name: "nav.privacy", to: "/privacy", dot: true },
    { name: "nav.contact", to: "/contact", dot: false },
]

function getCurrent() {
    const navigationObjects = [...baseNavigation, ...leadNavigation, ...secondaryNavigation]
    const response = navigationObjects.find((item) => item.name === settingsStore.current.pageName)
    if (response) return response
    return {} as INav
}

onMounted(() => {
    headingTerm.value = getCurrent()
})
</script>