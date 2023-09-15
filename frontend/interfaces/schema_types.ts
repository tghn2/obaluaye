export type IPathwayType = "PERSONAL" | "RESEARCH"

export type INodeType =
    | "VALUE"
    | "VALUERANGE"
    | "SCALE"
    | "BOOLEAN"
    | "SELECTONE"
    | "SELECTMANY"
    | "SELECTBRANCH"
    | "UPLOAD"

export type IResourceType =
    | "MARKDOWN"
    | "DOWNLOAD"
    | "WEBLINK"

export type IRoleType =
    | "CUSTODIAN"
    | "CURATOR"
    | "RESEARCHER"
    | "VIEWER"

export type IValueType =
    | "DATE"
    | "DATETIME"
    | "YEAR"
    | "NUMBER"
    | "INTEGER"
    | "BOOLEAN"
    | "ARRAY"
    | "STRING"


export type InvitationResponseType =
    | "WAITING"
    | "ACCEPTED"
    | "REFUSED"