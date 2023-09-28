import { ITheme, IFilters } from "@/interfaces"
import { apiCore } from "./core"

export const apiTheme = {
  async getMulti(token: string, payload: IFilters = {}) {
    return await useFetch<ITheme[]>(`${apiCore.url()}/theme/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<ITheme>(`${apiCore.url()}/theme/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, payload: ITheme) {
    return await useFetch<ITheme>(`${apiCore.url()}/theme/`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async updateTerm(token: string, key: string, payload: ITheme) {
    return await useFetch<ITheme>(`${apiCore.url()}/theme/${key}`, 
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<ITheme>(`${apiCore.url()}/theme/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
}