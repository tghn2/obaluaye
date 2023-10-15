import { IComment, IFilters } from "@/interfaces"
import { apiCore } from "./core"

export const apiComment = {
  async getMulti(token: string, payload: IFilters = {}) {
    return await useFetch<IComment[]>(`${apiCore.url()}/comment/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<IComment>(`${apiCore.url()}/comment/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, key: string, payload: IComment) {
    return await useFetch<IComment>(`${apiCore.url()}/comment/${key}`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<IComment>(`${apiCore.url()}/comment/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async resolveTerm(token: string, key: string) {
    return await useFetch<IComment>(`${apiCore.url()}/comment/${key}/resolve`, 
      {
        method: "PUT",
        headers: apiCore.headers(token),
      }
    )
  },
}