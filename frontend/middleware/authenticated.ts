import { useAuthStore } from "@/stores"

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  const localePath = useLocalePath()
  const routes = ["/login", "/join", "/recover-password", "/reset-password"]
  if (!authStore.loggedIn) {
    if (routes.includes(from.path)) return navigateTo(localePath("/"))
    else return abortNavigation()
  }
})