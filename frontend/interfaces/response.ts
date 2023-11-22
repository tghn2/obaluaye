import { IProfileSummary } from "./profile"
import { ISummary } from "./general"
import { IKeyable } from "./utilities"

export interface IResponse {
    // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    id?: string
    created?: string
    modified?: string
    language?: string
    answer?: IAnswer | IAnswer[]
    validated?: boolean
    node_id?: string
    comments?: number
    respondent?: ISummary
    respondent_id?: string
    group_id?: string
}

export interface IPostResponse {
    // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    id?: string
    created?: string
    modified?: string
    language?: string
    answer?: string
    validated?: boolean
    node_id?: string
    comments?: number
    respondent?: ISummary
    respondent_id?: string
    group_id?: string
}

export interface IAnswer {
    id?: string
    value?: string
    dtype?: string
    count?: number
}

export interface IAnswerResponse {
    // For use in FormResponse components for checking validation
    answer?: IAnswer | IAnswer[]
    validated?: boolean
}

export interface IComment {
    // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    id?: string
    created?: string
    modified?: string
    content?: string
    resolved?: boolean
    language?: string
    response_id?: string
    researcher_id?: string
    researcher?: IProfileSummary
    group?: ISummary
}