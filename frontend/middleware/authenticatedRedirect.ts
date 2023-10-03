import { useAuthStore } from "@/stores"

export default defineNuxtRouteMiddleware((to, from) => {
    const authStore = useAuthStore()
    const routes = ["/login", "/join", "/recover-password", "/reset-password"]
    // https://stackoverflow.com/a/66613374/295606
    const locale = app.i18n.locale === app.i18n.defaultLocale ? "" : "/" + app.i18n.locale
    if (!authStore.loggedIn) {
        if (routes.includes(from.path)) return navigateTo(locale + "/")
        else return abortNavigation()
    } else {
        const createRoute = to.path.includes("/edit") ? "create" : "edit/create"
        const id = to.params.id ? to.params.id : createRoute
        return navigateTo(locale + `${to.path}/${id}`)
    }
})