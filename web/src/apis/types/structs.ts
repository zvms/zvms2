import * as enums from "././enums";

export interface Class {
    name: string
}

export interface SingleClass {
    id: number,
    name: string
}

export interface SingleUserWithoutAuth {
    id: number,
    name: string
}

export interface SingleUser extends SingleUserWithoutAuth {
    auth: number
}

export type ListClassesResponse = Array<SingleClass>

export interface ClassInfoResponse {
    name: string,
    students: Array<SingleUser>,
    teachers: Array<SingleUser>
}

export interface UserLoginResponse {
    token: string
}

export type SearchUsersResponse = Array<SingleUser>

export interface UserInfoResponse {
    name: string,
    cls: number,
    auth: number,
    clsName: string
}

export interface PictureResponse {
    hash: string,
    type: string
}

export interface ThoughtInfoResponse {
    reason?: string,
    thought?: string,
    reward?: number,
    pics?: Array<PictureResponse>
}

export interface StudentThoughtsResponse {
    accepted: Array<ThoughtInfoResponse>,
    unsubmitted: Array<ThoughtInfoResponse>,
    draft: Array<ThoughtInfoResponse>,
    unaudited: Array<ThoughtInfoResponse>
}

export interface StudentStatResponse {
    inside: number,
    outside: number,
    large: number
}

export interface SingleNotice {
    id: number,
    title: string,
    content: string,
    sender: number,
    deadtime: string,
    senderName: string
}

export type SearchNoticesResponse = Array<SingleNotice>

export interface SingleSignup {
    volId: number,
    volName: string,
    stuId: number,
    stuName: string
}

export type ListSignupResponse = Array<SingleSignup>

export interface SingleVolunteer {
    id: number,
    name: string,
    time: string,
    status: number,
    signable: boolean
}

export type SearchVolunteersResponse = Array<SingleVolunteer>

export interface VolunteerInfoResponse {
    name: string,
    description: string,
    time: string,
    status: enums.VolStatus,
    type: enums.VolType,
    reward: number,
    signable: boolean,
    joiners: Array<SingleUserWithoutAuth>,
    holder: number,
    holderName: string
}

export interface SearchNotices {
    sender?: number,
    user?: number,
    cls?: number,
    school?: number
}

export interface NoticeBody {
    title: string,
    content: string,
    deadtime: string
}

export interface Notice extends NoticeBody {
    targets: Array<number>
}

export interface Report {
    report: string
}

export interface Signup {
    students: Array<number>
}

export interface SearchThoughts {
    cls?: number,
    status?: enums.ThoughtStatus,
    student?: number,
    volunteer?: number
}

export interface SingleThought {
    volId: number,
    stuId: number,
    status: enums.ThoughtStatus,
    stuName: string,
    volName: string
}

export type SearchThoughtsResponse = Array<SingleThought>

export interface Picture {
    base64: string,
    type: string
}

