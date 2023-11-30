<template>
    <!-- Profile dropdown -->
    <Menu as="div" class="relative ml-3">
        <div v-if="!authStore.loggedIn">
            <LocaleLink to="/login"
                class="rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-kashmir-500 focus:ring-offset-2">
                <PhSignIn class="block h-6 w-6" />
            </LocaleLink>
        </div>
        <div v-else>
            <MenuButton
                class="flex rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-kashmir-500 focus:ring-offset-2">
                <span class="sr-only">Open user menu</span>
                <div class="rounded-lg">
                    <PhUserCircle class="h-6 w-6 text-kashmir-500 shrink-0" alt="authStore.email" />
                </div>
            </MenuButton>
        </div>
        <transition enter-active-class="transition ease-out duration-200" enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
            <MenuItems
                class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <MenuItem v-for="(nav, i) in navigation" :key="`nav-${i}`" v-slot="{ active }">
                <LocaleLink :to="nav.to" :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">{{
                    nav.name }}
                </LocaleLink>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                <a :class="[active ? 'bg-gray-100 cursor-pointer' : '', 'block px-4 py-2 text-sm text-gray-700 cursor-pointer']"
                    @click="logout">
                    Logout
                </a>
                </MenuItem>
            </MenuItems>
        </transition>
    </Menu>
</template>

  
<script setup lang="ts">
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue"
import { PhSignIn, PhUserCircle } from "@phosphor-icons/vue"
import {
    useAuthStore, useToastStore, usePathwayStore, useGroupStore,
} from "@/stores"

const localePath = useLocalePath()
const authStore = useAuthStore()
const navigation = [
    { name: "Settings", to: "/settings" },
]
const redirectRoute = "/"

async function logout() {
    const toastStore = useToastStore()
    const pathwayStore = usePathwayStore()
    const groupStore = useGroupStore()
    toastStore.resetState()
    pathwayStore.resetState()
    groupStore.resetState()
    authStore.logOut()
    await navigateTo(localePath(redirectRoute))
}
</script>