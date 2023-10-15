import { IResource } from "@/interfaces"
import { apiCore } from "./core"

export const apiResource = {
  async getTerm(key: string) {
    return await useFetch<IResource>(`${apiCore.url()}/resource/${key}`)
  },
  async createTerm(token: string, key: string, payload: IResource) {
    return await useFetch<IResource>(`${apiCore.url()}/resource/${key}`, 
      {
        method: "POST",
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