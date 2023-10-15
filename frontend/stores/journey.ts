import { ITheme, IResponse } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { useAuthStore } from "./auth"
import { apiTheme, apiResponse } from "@/api"

export const useJourneyStore = defineStore("journeyStore", {
    state: () => ({
        one: {} as ITheme,
        savingEdit: false,
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        term: (state) => state.one,
        savingDraft: (state) => state.savingEdit,
        sourceKey: (state) => {
            return (
                state.one
                && (
                    (
                        state.one.group
                        && state.one.group.id
                    )
                    || (
                        useAuthStore().profile 
                        && useAuthStore().profile.id
                    )
                )
            )
        },
        sourceRespondent: (state) => {
            return (
                state.one
                && useAuthStore().profile
                && useAuthStore().profile.id
            )
        },
        sourceGroup: (state) =>  {
            return (
                state.one
                && state.one.group
                && state.one.group.id
            )
        },
        authTokens: () => {
            return ( useTokenStore() )
        },
        settings: () => {
            return ( useSettingStore() )
        },
    },
    actions: {
        async getTerm(key: string, manualState = true) {
            await this.authTokens.refreshTokens()
            try {
                this.settings.setPageState("loading")
                this.setTerm({} as ITheme)
                const { data: response } = await apiTheme.getTerm(this.authTokens.token, key, this.settings.locale)
                if (response.value) this.setTerm(response.value)
                if (manualState) this.settings.setPageState("done")
            } catch (error) {
                this.settings.setPageState("error")
            }
        },
        async createTerm(payload: IResponse[] = [] as IResponse[]) {
            // Saves all the responses for a single Theme simultaneously
            this.savingEdit = true
            await this.authTokens.refreshTokens()
            if (this.authTokens.token && payload.length) {
                try {
                    // Loop through responses to create and update these - add group, respondent & language
                    // https://stackoverflow.com/a/34349073/295606
                    for (const response of payload) {
                        response.respondent_id = this.sourceRespondent
                        response.group_id = this.sourceGroup
                        response.language = this.term.language
                        await apiResponse.createTerm(this.authTokens.token, response.id as string, response)
                    }
                } catch (error) {
                    const toasts = useToastStore()
                    toasts.addNotice({
                        title: "pathway.alert.saveErrorTitle",
                        content: "pathway.alert.saveErrorContent",
                        icon: "error"
                    })
                }
                this.savingEdit = false
            }
        },
        setSavingEdit(payload: boolean) {
            this.savingEdit = payload
        },
        setTerm(payload: ITheme) {
            this.one = payload
        },
        async removeTerm(key: string) {
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                    this.settings.setPageState("loading")
                    await apiResponse.removeTerm(this.authTokens.token, key)
                    this.settings.setPageState("done")
                } catch (error) {
                    this.settings.setPageState("error")
                    const toasts = useToastStore()
                    toasts.addNotice({
                            title: "pathway.alert.removeErrorTitle",
                            content: "pathway.alert.removeErrorContent",
                            icon: "error"
                        })
                }
            }
        },
        // reset state using `$reset`
        resetState () {
            this.$reset()
        }
    }
})