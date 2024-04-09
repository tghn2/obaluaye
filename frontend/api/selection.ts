import { ISelection, IFilters, IMsg } from "@/interfaces"
import { apiCore } from "./core"

export const apiSelection = {
    async getMulti(token: string, payload: IFilters = {}) {
        return await useFetch<ISelection[]>(`${apiCore.url()}/selection/`, 
            {
                query: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async getTerm(token: string, key: string, language: string) {
        return await useFetch<ISelection>(`${apiCore.url()}/selection/${key}`, 
            {
                query: { language },
                headers: apiCore.headers(token),
            }
        )
    },
    async createTerm(token: string, payload: ISelection) {
        return await useFetch<ISelection>(`${apiCore.url()}/selection/`, 
            {
                method: "POST",
                body: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async updateTerm(token: string, key: string, payload: ISelection) {
        return await useFetch<ISelection>(`${apiCore.url()}/selection/${key}`, 
            {
                method: "PUT",
                body: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async removeTerm(token: string, key: string) {
        return await useFetch<IMsg>(`${apiCore.url()}/selection/${key}`, 
            {
                method: "DELETE",
                headers: apiCore.headers(token),
            }
        )
    },
}