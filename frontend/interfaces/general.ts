import { IResourceType, IPathwayType } from "./schema_types"

export interface IResource {
    id?: string
    created?: string
    modified?: string
    name?: string
    title?: string
    description?: string
    content?: string
    resourceType?: IResourceType
    language?: string
    pathway_id?: string
    theme_id?: string
    node_id?: string
}

export interface IFilters {
    match?: string
    date_from?: string
    date_to?: string
    language?: string
    featured?: boolean
    complete?: boolean
    selections?: boolean
    path_type?: IPathwayType
    page?: number
}

export interface ISummary {
    id?: string
    created?: string
    modified?: string
    isPrivate?: boolean
    name?: string
    title?: string
    description?: string
    subjects?: string[]
    country?: string[]
    language?: string
    order?: number
    resources?: IResource[]
}