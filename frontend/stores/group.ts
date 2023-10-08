import { IGroup, IGroupRole, IGroupInvitation, IRoleType, IFilters } from "@/interfaces"
import { useTokenStore } from "./tokens"
import { useSettingStore } from "./settings"
import { useToastStore } from "./toasts"
import { useAuthStore } from "./auth"
import { apiGroup, apiAuth } from "@/api"

export const useGroupStore = defineStore("groupStore", {
  state: () => ({
    board: [] as IGroup[],
    one: {} as IGroup,
    edit: {} as IGroup,
    createEdit: false,
    invitationships: {} as IGroupInvitation[],
    memberships: {} as IGroupRole[],
    facets: {} as IFilters,
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    multi: (state) => state.board,
    term: (state) => state.one,
    draft: (state) => state.edit,
    invitations: (state) => state.invitationships,
    createDraft: (state) => state.createEdit,
    members: (state) => state.memberships,
    isResearcher: (state) => {
      const authStore = useAuthStore()
      return (
        state.one
        && state.one.roles
        && state.one.roles.length
        && state.one.roles.filter(member =>
          member.researcher.email === authStore.email
          && member.responsibility === "RESEARCHER").length === 1
      )
    },
    isCustodian: (state) => {
      const authStore = useAuthStore()
      return (
        state.one
        && state.one.roles
        && state.one.roles.length
        && state.one.roles.filter(member =>
          member.researcher.email === authStore.email
          && member.responsibility === "CUSTODIAN").length === 1
      )
    },
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
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setMulti([])
          if (!facets || Object.keys(facets).length === 0) facets = this.facets
          const { data: response } = await apiGroup.getMulti(this.authTokens.token, facets)
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
      }
    },
    setMulti(payload: IGroup[]) {
      this.board = payload
    },
    async getTerm(key: string, manualState = true) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setTerm({} as IGroup)
          const { data: response } = await apiGroup.getTerm(this.authTokens.token, key)
          if (response.value) this.setTerm(response.value)
          if (manualState) this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
        }
      }
    },
    // async createTerm(payload: IGroup = {} as IGroup) {
    //   await this.authTokens.refreshTokens()
    //   if (this.authTokens.token) {
    //     try {
    //       if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
    //       const { data: response } = await apiGroup.createTerm(this.authTokens.token, this.draft)
    //     //   if (response.value) {
    //     //     this.setTerm(response.value)
    //     //     this.resetDraft()
    //     //   } 
    //     } catch (error) {
    //     //   this.one = {} as IGroup
    //     }
    //   }
    // },
    async updateTerm(key: string, payload: IGroup = {} as IGroup) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          if (payload && Object.keys(payload).length !== 0) this.setDraft(payload)
          if (this.createEdit) await apiGroup.createTerm(this.authTokens.token, this.draft)
          else await apiGroup.updateTerm(this.authTokens.token, key, this.draft)
          this.createEdit = false
        } catch (error) {
            const toasts = useToastStore()
            toasts.addNotice({
                title: "group.alert.saveErrorTitle",
                content: "group.alert.saveErrorContent",
                icon: "error"
            })
        }
      }
    },
    setDraft(payload: IGroup) {
      this.edit = payload
    },
    resetDraft() {
      this.edit = {} as IGroup
    },
    setCreateDraft(payload: boolean) {
        this.createEdit = payload
    },
    setTerm(payload: IGroup) {
      this.one = payload
    },
    async removeTerm(key: string) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiGroup.removeTerm(this.authTokens.token, key)
          if (response.value) this.setTerm({} as IGroup)
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Deletion error",
            content: "Could not remove group. Please check your details, or internet connection, and try again.",
            icon: "error"
          })
        }
      }
    },
    async getMembers(key: string, facets: IFilters = {}) {
      // For the group
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiGroup.getAllMembers(this.authTokens.token, key, facets)
          if (response.value) {
            if (response.value.length) {
              this.setMembers(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.memberships = []
        }
      }
    },
    async getGroupRoles(facets: IFilters = {}) {
      // For the user
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          const { data: response } = await apiAuth.getAllMemberships(this.authTokens.token, facets)
          if (response.value) {
            if (response.value.length) {
              this.setMembers(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.memberships = []
        }
      }
    },
    async updateMember(key: string, member_key: string, role_type: IRoleType, facets: IFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiGroup.updateMember(this.authTokens.token, key, member_key, role_type, facets)
          if (response.value) this.setMembers(response.value)
        } catch (error) {
          this.memberships = []
        }
      }
    },
    async removeMember(key: string, member_key: string, facets: IFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiGroup.removeMember(this.authTokens.token, key, member_key, facets)
          if (response.value) this.setMembers(response.value)
        } catch (error) {
          this.memberships = []
        }
      }
    },
    setMembers(payload: IGroupRole[]) {
      this.memberships = payload
    },
    async getInvitations(key: string, facets: IFilters = {}) {
      // For group
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
          try {
            this.setInvitations([])
          const { data: response } = await apiGroup.getAllInvitations(this.authTokens.token, key, facets)
          if (response.value) {
            if (response.value.length) {
              this.setInvitations(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.invitationships = []
        }
      }
    },
    async getMembershipInvitations(facets: IFilters = {}) {
      // For user
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          this.settings.setPageState("loading")
          this.setInvitations([])
          const { data: response } = await apiAuth.getAllInvitations(this.authTokens.token, facets)
          if (response.value) {
            if (response.value.length) {
              this.setInvitations(response.value)
              this.settings.setPageNext(true)
            } else {
              this.settings.setPageNext(false)
            }
          }
          this.settings.setPageState("done")
        } catch (error) {
          this.settings.setPageState("error")
          this.invitationships = []
        }
      }
    },
    async createInvitation(key: string, email: string, facets: IFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const toasts = useToastStore()
          const { data: response } = await apiGroup.createInvitation(this.authTokens.token, key, email, facets)
          if (response.value) {
            this.setInvitations(response.value)
            toasts.addNotice({
              title: "Member invitation",
              content: `Remember to email ${email} to invite them yourself and tell them about this group.`,
            })
          } else toasts.addNotice({
            title: "Invitation error",
            content: `You have already invited ${email}.`,
            icon: "error"
          })
        } catch (error) {
          const toasts = useToastStore()
          toasts.addNotice({
            title: "Invitation error",
            content: error as string,
            icon: "error"
          })
        }
      }
    },
    async removeInvitation(key: string, invitation_key: string, facets: IFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiGroup.removeInvitation(this.authTokens.token, key, invitation_key, facets)
          if (response.value) this.setInvitations(response.value)
        } catch (error) {
          this.invitationships = []
        }
      }
    },
    async acceptInvitation(invitation_key: string, facets: IFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiAuth.acceptInvitation(this.authTokens.token, invitation_key, facets)
          if (response.value) this.setInvitations(response.value)
        } catch (error) {
          this.invitationships = []
        }
      }
    },
    async rejectInvitation(invitation_key: string, facets: IFilters = {}) {
      await this.authTokens.refreshTokens()
      if (this.authTokens.token) {
        try {
          const { data: response } = await apiAuth.rejectInvitation(this.authTokens.token, invitation_key, facets)
          if (response.value) this.setInvitations(response.value)
        } catch (error) {
          this.invitationships = []
        }
      }
    },
    setInvitations(payload: IGroupInvitation[]) {
      this.invitationships = payload
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