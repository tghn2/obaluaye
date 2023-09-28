import { IResource, IFilters } from "@/interfaces"
import { apiCore } from "./core"

export const apiResource = {
  async getMulti(token: string, payload: IFilters = {}) {
    return await useFetch<IResource[]>(`${apiCore.url()}/resource/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<IResource>(`${apiCore.url()}/resource/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, payload: IResource) {
    return await useFetch<IResource>(`${apiCore.url()}/resource/`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async updateTerm(token: string, key: string, payload: IResource) {
    return await useFetch<IResource>(`${apiCore.url()}/resource/${key}`, 
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IResource>(`${apiCore.url()}/resource/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
}