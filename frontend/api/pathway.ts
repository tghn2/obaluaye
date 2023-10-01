import { IPathway, IFilters, IMsg, IKeyable } from "@/interfaces"
import { apiCore } from "./core"

export const apiPathway = {
    async getMulti(payload: IFilters = {}) {
        return await useFetch<IPathway[]>(`${apiCore.url()}/pathway/`, 
        {
            query: payload,
        }
        )
    },
    async getTerm(key: string, language: string) {
        return await useFetch<IPathway>(`${apiCore.url()}/pathway/${key}`, 
        {
            query: { language },
        }
        )
    },
    async createTerm(token: string, payload: IPathway) {
        return await useFetch<IPathway>(`${apiCore.url()}/pathway/`, 
        {
            method: "POST",
            body: payload,
            headers: apiCore.headers(token),
        }
        )
    },
    async updateTerm(token: string, key: string, payload: IPathway) {
        return await useFetch<IPathway>(`${apiCore.url()}/pathway/${key}`, 
        {
            method: "PUT",
            body: payload,
            headers: apiCore.headers(token),
        }
        )
    },
    async toggleTerm(token: string, key: string, payload: IPathway) {
        return await useFetch<IMsg>(`${apiCore.url()}/pathway/${key}/toggle-state`, 
        {
            method: "PUT",
            body: payload,
            headers: apiCore.headers(token),
        }
        )
    },
    async getSchemaDownload(key: string, language: string) {
        return await useFetch<IKeyable>(`${apiCore.url()}/pathway/${key}/download`,
            {
                query: { language },
            }
        )
    },
    async removeTerm(token: string, key: string) {
        return await useFetch<IPathway>(`${apiCore.url()}/pathway/${key}`, 
        {
            method: "DELETE",
            headers: apiCore.headers(token),
        }
        )
    },
}