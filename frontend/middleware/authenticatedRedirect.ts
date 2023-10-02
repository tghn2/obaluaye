import { useAuthStore } from "@/stores"

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  const localePath = useLocalePath()
  const routes = ["/login", "/join", "/recover-password", "/reset-password"]
  if (!authStore.loggedIn) {
    if (routes.includes(from.path)) return navigateTo(localePath("/"))
    else return abortNavigation()
  } else {
    const createRoute = to.path.includes("/edit") ? "create" : "edit/create"
    const id = to.params.id ? to.params.id : createRoute
    return navigateTo(localePath(`${to.path}/${id}`))
  }
})