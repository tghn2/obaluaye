export interface ISelection {
    id?: string
    created?: string
    modified?: string
    term?: string
    language?: string
    collection_id?: string
}

export interface ICollection {
    id?: string
    created?: string
    modified?: string
    name?: string
    title?: string
    language?: string
    isMulti?: boolean
    selection?: ISelection[]
}
