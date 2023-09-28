import { INode, IFilters } from "@/interfaces"
import { apiCore } from "./core"

export const apiNode = {
  async getMulti(token: string, payload: IFilters = {}) {
    return await useFetch<INode[]>(`${apiCore.url()}/node/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getTerm(token: string, key: string) {
    return await useFetch<INode>(`${apiCore.url()}/node/${key}`, 
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async createTerm(token: string, payload: INode) {
    return await useFetch<INode>(`${apiCore.url()}/node/`, 
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async updateTerm(token: string, key: string, payload: INode) {
    return await useFetch<INode>(`${apiCore.url()}/node/${key}`, 
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeTerm(token: string, key: string) {
    return await useFetch<INode>(`${apiCore.url()}/node/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
}