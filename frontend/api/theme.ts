import { ITheme } from "@/interfaces"
import { apiCore } from "./core"

export const apiTheme = {
    async getTerm(token: string = "", key: string, language: string) {
        if (token) return await useFetch<ITheme>(`${apiCore.url()}/theme/${key}`, 
            {
                query: { language },
                headers: apiCore.headers(token),
            }
        )
        else return await useFetch<ITheme>(`${apiCore.url()}/theme/${key}`, 
            {
                query: { language },
            }
        )
    },
    async createTerm(token: string, key: string, payload: ITheme) {
        return await useFetch<ITheme>(`${apiCore.url()}/theme/${key}`, 
            {
                method: "POST",
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