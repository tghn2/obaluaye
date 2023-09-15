import { IResource } from "./general"

export interface ITheme {
    // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    id?: string
    order?: number
    created?: string
    modified?: string
    name?: string
    title?: string
    description?: string
    subjects?: string[]
    country?: string[]
    spatial?: string
    language?: string
    pathway_id?: string
    resources?: IResource[]
}