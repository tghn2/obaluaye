import { IGroup, IFilters } from "@/interfaces"
import { useSettingStore } from "./settings"
import { apiGroup, } from "@/api"

export const useSearchStore = defineStore("searchStore", {
  state: () => ({
    board: [] as IGroup[],
    one: {} as IGroup,
    facets: {} as IFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    multi: (state) => state.board,
    term: (state) => state.one,
    filters: (state) => state.facets,
    settings: () => {
      return ( useSettingStore() )
    },
  },
  actions: {
    async getMulti(facets: IFilters = {}) {
        try {
        //   this.settings.setPageState("loading")
        //   this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiGroup.getSearch(facets)
          if (response.value) {
            if (response.value.length) {
              this.setMulti(response.value)
              this.settings.setPageNext(true)
            } else {
              this.setMulti([])
              this.settings.setPageNext(false)
            }
          }
        //   this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.board = []
        }
    },
    async getTerm(key: string, manualState = true) {
        try {
          if (manualState) this.settings.setPageState("loading")
          this.setTerm({} as IGroup)
          const { data: response } = await apiGroup.getSearchTerm(key)
          if (response.value) this.setTerm(response.value)
          if (manualState) this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
        }
    },
    setMulti(payload: IGroup[]) {
      this.board = payload
    },
    setFilters(payload: IFilters) {
      this.facets = payload
    },
    setTerm(payload: IGroup) {
      this.one = payload
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