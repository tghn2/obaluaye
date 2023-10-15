import {
    INodeType,
    IPathwayType,
    IResourceType,
    IRoleType,
    IValueType,
    InvitationResponseType
} from "./schema_types"

import { ISummary, IResource, IFilters } from "./general"

import {
    IUserProfile,
    IUserProfileUpdate,
    IUserProfileCreate,
    IUserOpenProfileCreate,
    IProfileSummary
} from "./profile"

import {
    ITokenResponse,
    IWebToken,
    INewTOTP,
    IEnableTOTP,
    ISendEmail,
    IMsg,
    INotification
} from "./utilities"

import { IGroup, IGroupFilters, IGroupInvitation, IGroupRole } from "./group"
import { IResponse, IPostResponse, IAnswer, IAnswerResponse, IComment } from "./response"
import { INode, IConstraints, IForm, ITerm } from "./node"
import { ITheme } from "./theme"
import { IPathway } from "./pathway"

// https://stackoverflow.com/a/64782482/295606
interface IKeyable {
    [key: string]: any | any[]
}
  
export {
    INodeType,
    IPathwayType,
    IResourceType,
    IRoleType,
    IValueType,
    InvitationResponseType,
    ISummary,
    IResource,
    IFilters,
    IKeyable,
    IUserProfile,
    IUserProfileUpdate,
    IUserProfileCreate,
    IUserOpenProfileCreate,
    IProfileSummary,
    ITokenResponse,
    IWebToken,
    INewTOTP,
    IEnableTOTP,
    ISendEmail,
    IMsg,
    INotification,
    IGroup,
    IGroupFilters,
    IGroupInvitation,
    IGroupRole,
    IResponse,
    IPostResponse,
    IAnswer,
    IAnswerResponse,
    IComment,
    INode,
    IConstraints,
    IForm,
    ITerm,
    ITheme,
    IPathway,
}