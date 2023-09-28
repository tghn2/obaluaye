import { IPathwayType } from "./schema_types"
import { IResource } from "./general"
import { ITheme } from "./theme"
import { INode } from "./node"

export interface IPathway {
    // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    id?: string
    created?: string
    modified?: string
    isPrivate: boolean
    isProtected: boolean
    name?: string
    title?: string
    description?: string
    pathType: IPathwayType
    subjects?: string[]
    country?: string[]
    spatial?: string
    temporalStart?: string
    temporalEnd?: string
    language?: string
    bibliographicCitation?: string
    themes?: ITheme[]
    resources?: IResource[]
}