import { IResponse, IKeyable, IMsg } from "@/interfaces"
import { apiCore } from "./core"

export const apiResponse = {
    async getTerm(key: string) {
        return await useFetch<IResponse>(`${apiCore.url()}/response/${key}`)
    },
    async createTerm(token: string, key: string, payload: IResponse) {
        return await useFetch<IResponse>(`${apiCore.url()}/response/${key}`, 
            {
                method: "POST",
                body: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async removeTerm(token: string, key: string) {
        return await useFetch<IResponse>(`${apiCore.url()}/response/${key}`, 
            {
                method: "DELETE",
                headers: apiCore.headers(token),
            }
        )
    },
    async getUploadTerm(folder_key: string, source_key: string) {
        return await useFetch<IKeyable>(`${apiCore.url()}/response/upload/${folder_key}/${source_key}`)
    },
    async createUploadTerm(token: string, payload: FormData, folder_key: string, source_key: string) {
        return await useFetch<IMsg>(`${apiCore.url()}/response/upload/${folder_key}/${source_key}`, 
            {
                method: "POST",
                body: payload,
                headers: apiCore.headers(token),
            }
        )
    },
    async removeUploadTerm(token: string, folder_key: string, source_key: string) {
        return await useFetch<IMsg>(`${apiCore.url()}/response/upload/${folder_key}/${source_key}`, 
            {
                method: "DELETE",
                headers: apiCore.headers(token),
            }
        )
    },
}