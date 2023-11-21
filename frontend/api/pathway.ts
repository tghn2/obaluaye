import { IPathway, IFilters, IMsg, IKeyable } from "@/interfaces"
import { apiCore } from "./core"

export const apiPathway = {
    async getMulti(token: string = "", payload: IFilters = {}) {
        if (token) return await useFetch<IPathway[]>(`${apiCore.url()}/pathway/`,
            {
                query: payload,
                headers: apiCore.headers(token),
            }
        )
        else return await useFetch<IPathway[]>(`${apiCore.url()}/pathway/`,
            {
                query: payload,
            }
        )
    },
    async getTerm(token: string = "", key: string, language: string) {
        if (token) return await useFetch<IPathway>(`${apiCore.url()}/pathway/${key}`, 
            {
                query: { language },
                headers: apiCore.headers(token),
            }
        )
        else return await useFetch<IPathway>(`${apiCore.url()}/pathway/${key}`, 
            {
                query: { language },
            }
        )
    },
    async getFeaturedTerm(language: string) {
        return await useFetch<IPathway>(`${apiCore.url()}/pathway/featured`, 
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
    async toggleTermFeatured(token: string, key: string) {
        return await useFetch<IMsg>(`${apiCore.url()}/pathway/${key}/featured`, 
            {
                method: "PUT",
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
    async createImportTerm(token: string, payload: IPathway) {
        return await useFetch<IPathway>(`${apiCore.url()}/pathway/import`, 
            {
                method: "POST",
                body: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async updateImportTerm(token: string, key: string, payload: IPathway) {
        return await useFetch<IPathway>(`${apiCore.url()}/pathway/import/${key}`, 
            {
                method: "PUT",
                body: payload,
                headers: apiCore.headers(token),
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