import { INodeType, IValueType } from "./schema_types"
import { IResource } from "./general"
import { ISummary } from "./general"

export interface INode {
    // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    id?: string
    order?: number
    created?: string
    modified?: string
    question?: string
    formType?: INodeType
    form?: IForm
    subjects?: string[]
    country?: string[]
    language?: string
    theme_id?: string
    theme?: ISummary
    pathway_id?: string
    pathway?: ISummary
    resources?: IResource[]
}

export interface ITerm {
    id?: string
    value?: string
    label?: string
    branch?: string
}

export interface IConstraints {
    dtype?: IValueType
    limit?: number
    range?: boolean
    minimum?: number
    maximum?: number
}

export interface IForm {
    formType?: INodeType
    required?: boolean
    randomise?: boolean
    terms?: ITerm[]
    constraints?: IConstraints
    example?: string
}