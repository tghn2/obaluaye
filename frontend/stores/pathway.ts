import { IPathway, IFilters } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiPathway, apiTheme, apiNode, apiResource } from "@/api"

export const usePathwayStore = defineStore("pathwayStore", {
    state: () => ({
        board: [] as IPathway[],
        one: {} as IPathway,
        edit: {} as IPathway,
        activeEdit: "" as string,
        translatingEdit: false,
        languageEdit: "" as string,
        createEdit: false,
        savingEdit: false,
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
        createDraft: (state) => state.createEdit,
        savingDraft: (state) => state.savingEdit,
        isTranslatingDraft: (state) => state.edit.language !== state.languageEdit,
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
                const { data: response } = await apiPathway.getMulti(this.authTokens.token, facets)
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
                const { data: response } = await apiPathway.getTerm(this.authTokens.token, key, this.settings.locale)
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
            this.savingEdit = true
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                    if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
                    // Make sure the language is as expected
                    this.edit.language = this.languageDraft
                    if (this.createEdit)
                        await apiPathway.createTerm(this.authTokens.token, this.draft)
                    else
                        await apiPathway.updateTerm(this.authTokens.token, key, this.draft)
                    this.createEdit = false
                    // Loop through themes and nodes to create and update these
                    // https://stackoverflow.com/a/34349073/295606
                    if (this.draft.resources && this.draft.resources.length) {
                        for (const resource of this.draft.resources) {
                            resource.pathway_id = this.draft.id
                            resource.language = this.draft.language
                            await apiResource.updateTerm(this.authTokens.token, resource.id as string, resource)
                        }
                    }
                    if (this.draft.themes && this.draft.themes.length) {
                        for (const [themeIdx, theme] of this.draft.themes.entries()) {
                            theme.pathway_id = this.draft.id
                            theme.order = themeIdx
                            theme.language = this.draft.language
                            const { data: themeResponse } = await apiTheme.updateTerm(this.authTokens.token, theme.id as string, theme)
                            if (theme.resources && theme.resources.length) {
                                for (const resource of theme.resources) {
                                    resource.pathway_id = this.draft.id
                                    resource.theme_id = theme.id
                                    resource.language = this.draft.language
                                    await apiResource.updateTerm(this.authTokens.token, resource.id as string, resource)
                                }
                            }
                            if (themeResponse.value && theme.nodes && theme.nodes.length) {
                                for (const [nodeIdx, node] of theme.nodes.entries()) {
                                    node.pathway_id = this.draft.id
                                    node.theme_id = theme.id
                                    node.order = nodeIdx
                                    node.language = this.draft.language
                                    const { data: nodeResponse } = await apiNode.updateTerm(this.authTokens.token, node.id as string, node)
                                    if (node.resources && node.resources.length) {
                                        for (const resource of node.resources) {
                                            resource.pathway_id = this.draft.id
                                            resource.node_id = node.id
                                            resource.language = this.draft.language
                                            await apiResource.updateTerm(this.authTokens.token, resource.id as string, resource)
                                        }
                                    }
                                }
                            }
                        }
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
        async toggleTerm(key: string) {
            this.savingEdit = true
            const toasts = useToastStore()
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                    if (Object.keys(this.term).length && this.term.id === key) {
                        const payload: IPathway = { ... this.term }
                        payload.isPrivate = payload.isPrivate ? false : true
                        const { data: response } = await apiPathway.toggleTerm(this.authTokens.token, key, payload)
                        if (response.value) this.one.isPrivate = payload.isPrivate
                    }
                    toasts.addNotice({
                        title: "pathway.alert.toggleSuccessTitle",
                        content: "pathway.alert.toggleSuccessContent",
                    })
                } catch (error) {
                    toasts.addNotice({
                        title: "pathway.alert.saveErrorTitle",
                        content: "pathway.alert.saveErrorContent",
                        icon: "error"
                    })
                }
            }
            this.savingEdit = false
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
        setCreateDraft(payload: boolean) {
            this.createEdit = payload
        },
        setLanguageDraft(payload: string) {
            // this.edit.language = payload
            this.languageEdit = payload
        },
        setIsTranslatingDraft(payload: boolean) {
            this.translatingEdit = payload
        },
        setSavingEdit(payload: boolean) {
            this.savingEdit = payload
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
                            title: "pathway.alert.removeErrorTitle",
                            content: "pathway.alert.removeErrorContent",
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