import { IGroup, IGroupFilters, IGroupInvitation, IGroupRole, IRoleType  } from "@/interfaces"
import { apiCore } from "./core"

export const apiGroup = {
  async getMulti(token: string, payload: IGroupFilters = {}) {
    return await useFetch<IGroup[]>(`${apiCore.url()}/group/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<IGroup>(`${apiCore.url()}/group/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, payload: IGroup) {
    return await useFetch<IGroup>(`${apiCore.url()}/group/`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async updateTerm(token: string, key: string, payload: IGroup) {
    return await useFetch<IGroup>(`${apiCore.url()}/group/${key}`, 
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IGroup>(`${apiCore.url()}/group/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  // MANAGE GROUP MEMBERS
  async getAllMembers(token: string, key: string, payload: IGroupFilters = {}) {
    return await useFetch<IGroupRole[]>(`${apiCore.url()}/project/${key}/members`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async updateMember(token: string, key: string, member_key: string, role_type: IRoleType, payload: IGroupFilters = {}) {
    return await useFetch<IGroupRole[]>(`${apiCore.url()}/project/${key}/members/${member_key}/${role_type}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async removeMember(token: string, key: string, member_key: string, payload: IGroupFilters = {}) {
    return await useFetch<IGroupRole[]>(`${apiCore.url()}/project/${key}/members/${member_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getAllInvitations(token: string, key: string, payload: IGroupFilters = {}) {
    return await useFetch<IGroupInvitation[]>(`${apiCore.url()}/project/${key}/invitations`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async createInvitation(token: string, key: string, email: string, payload: IGroupFilters = {}) {
    return await useFetch<IGroupInvitation[]>(`${apiCore.url()}/project/${key}/invitations/${email}`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async removeInvitation(token: string, key: string, invitation_key: string, payload: IGroupFilters = {}) {
    return await useFetch<IGroupInvitation[]>(`${apiCore.url()}/project/${key}/invitations/${invitation_key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
}