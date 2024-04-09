import { ICollection, IFilters, IMsg } from "@/interfaces"
import { apiCore } from "./core"

export const apiCollection = {
    async getMulti(token: string, payload: IFilters = {}) {
        return await useFetch<ICollection[]>(`${apiCore.url()}/collection/`, 
            {
                query: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async getTerm(token: string, key: string, language: string) {
        return await useFetch<ICollection>(`${apiCore.url()}/collection/${key}`, 
            {
                query: { language },
                headers: apiCore.headers(token),
            }
        )
    },
    async createTerm(token: string, payload: ICollection) {
        return await useFetch<ICollection>(`${apiCore.url()}/collection/`, 
            {
                method: "POST",
                body: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async updateTerm(token: string, key: string, payload: ICollection) {
        return await useFetch<ICollection>(`${apiCore.url()}/collection/${key}`, 
            {
                method: "PUT",
                body: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async removeTerm(token: string, key: string) {
        return await useFetch<IMsg>(`${apiCore.url()}/collection/${key}`, 
            {
                method: "DELETE",
                headers: apiCore.headers(token),
            }
        )
    },
}