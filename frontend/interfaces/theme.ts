import { IResource, ISummary } from "./general"
import { INode } from "./node"

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
    pathway?: ISummary
    group?: ISummary
    resources?: IResource[]
    nodes?: INode[]
    journeyPath?: string[]
}