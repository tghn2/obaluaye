import { IProfileSummary } from "./profile"
import { InvitationResponseType, IRoleType } from "./schema_types"
import { ISummary } from "./general"
import { IResponse } from "./response"

export interface IGroup {
    // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    id?: string
    created?: string
    modified?: string
    name?: string
    title?: string
    description?: string
    subjects?: string[]
    country?: string[]
    spatial?: string
    language?: string
    pathway?: ISummary
    pathway_id?: string
    members?: IGroupRole[]
    invitations?: IGroupInvitation[]
    responses?: IResponse[]
}

export interface IGroupFilters {
    match?: string
    descending?: boolean
    page?: number
}
  
export interface IGroupRole {
    id: string
    created: string
    researcher: IProfileSummary
    researcher_id?: string
    group_id?: string
    pathway_id?: string
    responsibility: IRoleType
  }
  
  export interface IGroupInvitation {
    id: string
    created: string
    full_name?: string
    email: string
    response: InvitationResponseType
    sender: IProfileSummary
    group?: ISummary
    group_id?: string
    pathway?: ISummary
    pathway_id?: string
  }