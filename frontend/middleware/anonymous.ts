import { useAuthStore } from "@/stores"

export default defineNuxtRouteMiddleware((to, from) => {
  const routes = ["/login", "/join", "/recover-password", "/reset-password"]
  const authStore = useAuthStore()
  if (authStore.loggedIn) {
    const locale = app.i18n.locale === app.i18n.defaultLocale ? "" : "/" + app.i18n.locale
    if (routes.includes(from.path)) return navigateTo(locale + "/")
    else return abortNavigation()
  }
})