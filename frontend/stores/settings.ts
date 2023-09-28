import { IPageStatusType } from "@/interfaces"

export const useSettingStore = defineStore("settingStore", {
  state: () => ({
        pageName: "" as string,
        pageState: "idle" as IPageStatusType,
        pageNext: true as boolean,
        currentLocale: "en" as string,
  }),
  persist: {
    storage: persistedState.cookiesWithOptions({
      // https://prazdevs.github.io/pinia-plugin-persistedstate/frameworks/nuxt-3.html
      // https://nuxt.com/docs/api/composables/use-cookie#options
      // in seconds
      // useRuntimeConfig().public.appCookieExpire,
      path: "/",
      secure: true,
      maxAge: 60 * 60 * 24 * 90,
      expires: new Date(new Date().getTime() + 60 * 60 * 24 * 90),
    }),
  },
    getters: {
        current: (state) => state,
        locale: (state) => state.currentLocale,
  },
    actions: {
        setPageName(payload: string) {
            this.pageName = payload
        },
        setPageState (payload: IPageStatusType) {
            this.pageState = payload
        },
        setPageNext(payload: boolean) {
            this.pageNext = payload
        },
        setCurrentLocale(payload: string) {
            this.currentLocale = payload
        },
        // reset state using `$reset`
        resetState () {
            this.$reset()
        }
  }
})