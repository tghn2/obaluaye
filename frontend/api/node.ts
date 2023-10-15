import { INode } from "@/interfaces"
import { apiCore } from "./core"

export const apiNode = {
  async createTerm(token: string, key: string, payload: INode) {
    return await useFetch<INode>(`${apiCore.url()}/node/${key}`, 
      {
        method: "POST",
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