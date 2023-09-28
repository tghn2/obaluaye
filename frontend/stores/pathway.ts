import { IPathway, IFilters } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiPathway } from "@/api"

export const usePathwayStore = defineStore("pathwayStore", {
    state: () => ({
        board: [] as IPathway[],
        one: {} as IPathway,
        edit: {} as IPathway,
        activeEdit: "" as string,
        translatingEdit: false,
        languageEdit: "" as string,
        facets: {} as IFilters,
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        multi: (state) => state.board,
        term: (state) => state.one,
        draft: (state) => state.edit,
        activeDraft: (state) => state.activeEdit,
        languageDraft: (state) => state.languageEdit,
        isTranslatingDraft: (state) => state.translatingEdit,
        filters: (state) => state.facets,
        authTokens: () => {
        return ( useTokenStore() )
        },
        settings: () => {
        return ( useSettingStore() )
        },
    },
    actions: {
        async getMulti(facets: IFilters = {}) {
            await this.authTokens.refreshTokens()
            try {
                this.settings.setPageState("loading")
                this.setMulti([])
                if (!facets || Object.keys(facets).length === 0) facets = this.facets
                facets.language = this.settings.locale
                const { data: response } = await apiPathway.getMulti(facets)
                if (response.value) {
                    if (response.value.length) {
                        this.setMulti(response.value)
                        this.settings.setPageNext(true)
                    } else {
                        this.settings.setPageNext(false)
                    }
                }
                this.settings.setPageState("done")
            } catch (error) {
                this.settings.setPageState("error")
                this.board = []
            }
        },
        setMulti(payload: IPathway[]) {
            this.board = payload
        },
        async getTerm(key: string, manualState = true) {
            await this.authTokens.refreshTokens()
            try {
                this.settings.setPageState("loading")
                this.setTerm({} as IPathway)
                const { data: response } = await apiPathway.getTerm(key, this.settings.locale)
                if (response.value) this.setTerm(response.value)
                if (manualState) this.settings.setPageState("done")
            } catch (error) {
                this.settings.setPageState("error")
            }
        },
        async createTerm(payload: IPathway = {} as IPathway) {
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
                const { data: response } = await apiPathway.createTerm(this.authTokens.token, this.draft)
                if (response.value) {
                    this.setTerm(response.value)
                    this.resetDraft()
                } 
                } catch (error) {
                this.one = {} as IPathway
                }
            }
        },
        async updateTerm(key: string, payload: IPathway = {} as IPathway) {
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
                const { data: response } = await apiPathway.updateTerm(this.authTokens.token, key, this.draft)
                if (response.value) {
                    this.setTerm(response.value)
                    this.resetDraft()
                } 
                } catch (error) {
                this.one = {} as IPathway
                }
            }
        },
        setDraft(payload: IPathway) {
            this.edit = payload
        },
        resetDraft() {
            this.edit = {} as IPathway
        },
        setActiveDraft(payload: string) {
            this.activeEdit = payload
        },
        setLanguageDraft(payload: string) {
            // this.edit.language = payload
            this.languageEdit = payload
        },
        setIsTranslatingDraft(payload: boolean) {
            this.translatingEdit = payload
        },
        setTerm(payload: IPathway) {
            this.one = payload
        },
        async removeTerm(key: string) {
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                this.settings.setPageState("loading")
                const { data: response } = await apiPathway.removeTerm(this.authTokens.token, key)
                if (response.value) this.setTerm({} as IPathway)
                this.settings.setPageState("done")
                } catch (error) {
                this.settings.setPageState("error")
                const toasts = useToastStore()
                toasts.addNotice({
                    title: "Deletion error",
                    content: "Could not remove pathway. Please check your details, or internet connection, and try again.",
                    icon: "error"
                })
                }
            }
        },
        setFilters(payload: IFilters) {
            this.facets = payload
        },
        setPage(payload: string) {
            if (!isNaN(+payload)) {
                this.facets.page = +payload 
            }
        },
        resetFilters() {
            const page = this.facets.page
            this.facets = {}
            this.setPage("" + page)
        },
        // reset state using `$reset`
        resetState () {
            this.$reset()
        }
    }
})