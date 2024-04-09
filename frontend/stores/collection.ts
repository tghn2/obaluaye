import { ISelection, ICollection, IFilters} from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { apiSelection, apiCollection } from "@/api"

export const useCollectionStore = defineStore("collectionStore", {
    state: () => ({
        board: [] as ICollection[],
        one: {} as ICollection,
        edit: {} as ICollection,
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
        languageDraft: (state) => state.languageEdit,
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
                const { data: response } = await apiCollection.getMulti(this.authTokens.token, facets)
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
        setMulti(payload: ICollection[]) {
            this.board = payload
        },
        async getTerm(key: string, manualState = true) {
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                    if (manualState) this.settings.setPageState("loading")
                    this.setTerm({} as ICollection)
                    const { data: response } = await apiCollection.getTerm(this.authTokens.token, key, this.settings.locale)
                    if (response.value) this.setTerm(response.value)
                    if (manualState) this.settings.setPageState("done")
                } catch (error) {
                    this.settings.setPageState("error")
                }
            }
        },
        setTerm(payload: ICollection) {
            this.one = payload
        },
        async createTerm(key: string, payload: ICollection) {
            this.savingEdit = true
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                    if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
                    // Make sure the language is as expected
                    this.edit.language = this.languageDraft
                    if (this.createEdit)
                        await apiCollection.createTerm(this.authTokens.token, this.draft)
                    else
                        await apiCollection.updateTerm(this.authTokens.token, key, this.draft)
                    if (this.draft.selection && this.draft.selection.length) {
                        for (const selection of this.draft.selection) {
                            selection.collection_id = this.draft.id
                            selection.language = this.draft.language
                            if (selection.id)
                                await apiSelection.updateTerm(this.authTokens.token, selection.id, selection)
                            else
                                await apiSelection.createTerm(this.authTokens.token, selection)
                        }
                        await this.getTerm(this.draft.id as string)
                    }
                    this.createEdit = false
                } catch (error) {
                    const toasts = useToastStore()
                    toasts.addNotice({
                        title: "pathway.alert.saveErrorTitle",
                        content: "pathway.alert.saveErrorContent",
                        icon: "error"
                    })
                }
            }
            this.savingEdit = false
        },
        async removeTerm(key: string) {
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                    this.settings.setPageState("loading")
                    await apiCollection.removeTerm(this.authTokens.token, key)
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
        async createTermSelection(key: string, payload: ISelection) {
            this.savingEdit = true
            await this.authTokens.refreshTokens()
            if (this.authTokens.token && payload.collection_id) {
                try {
                    // if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
                    // Make sure the language is as expected
                    this.edit.language = this.languageDraft
                    if (this.createEdit)
                        await apiSelection.createTerm(this.authTokens.token, payload)
                    else
                        await apiSelection.updateTerm(this.authTokens.token, key, payload)
                    this.createEdit = false
                    await this.getTerm(payload.collection_id)
                } catch (error) {
                    const toasts = useToastStore()
                    toasts.addNotice({
                        title: "pathway.alert.saveErrorTitle",
                        content: "pathway.alert.saveErrorContent",
                        icon: "error"
                    })
                }
            }
            this.savingEdit = false
        },
        async removeTermSelection(key: string, collectionId: string) {
            await this.authTokens.refreshTokens()
            if (this.authTokens.token) {
                try {
                    this.settings.setPageState("loading")
                    await apiSelection.removeTerm(this.authTokens.token, key)
                    await this.getTerm(collectionId)
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
        setLanguageDraft(payload: string) {
            this.languageEdit = payload
        },
        setCreateDraft(payload: boolean) {
            this.createEdit = payload
        },
        setDraft(payload: ICollection) {
            this.edit = payload
        },
        resetDraft() {
            this.edit = {} as ICollection
        },
        // reset state using `$reset`
        resetState () {
            this.$reset()
        }
    }
})