import { IProfileSummary } from "./profile"
import { ISummary } from "./general"

export interface IResponse {
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
    answer?: IAnswer
    node_id?: string
    comments?: IComment[]
    respondent?: ISummary
    respondent_id?: string
    group?: ISummary
    group_id?: string
    pathway?: ISummary
    pathway_id?: string
}

export interface IAnswer {
    id?: string
    value?: string
    dtype?: string
}

export interface IComment {
    // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    id?: string
    order?: number
    created?: string
    modified?: string
    content?: string
    resolved?: boolean
    language?: string
    response_id?: string
    creator_id?: string
    creator?: IProfileSummary
}