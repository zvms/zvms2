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

export type ListClassesResponse = SingleClass[]

export interface ClassInfoResponse {
    name: string,
    students: SingleUser[],
    teachers: SingleUser[]
}

export interface UserLoginResponse {
    token: string
}

export type SearchUsersResponse = SingleUser[]

export interface UserInfoResponse {
    name: string,
    cls: number,
    auth: number,
    clsName: string
}

export interface ThoughtInfoResponse {
    reason: string,
    thought: string,
    reward: number,
    pics: string[]
}

export interface StudentThoughtsResponse {
    accepted: ThoughtInfoResponse[],
    unsubmitted: ThoughtInfoResponse[],
    draft: ThoughtInfoResponse[],
    unaudited: ThoughtInfoResponse[]
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

export type SearchNoticesResponse = SingleNotice[]

export interface SingleSignup {
    volId: number,
    volName: string,
    stuId: number,
    stuName: string
}

export type ListSignupResponse = SingleSignup[]

export interface SingleVolunteer {
    id: number,
    name: string,
    time: string,
    status: number
}

export type SearchVolunteersResponse = SingleVolunteer[]

export interface VolunteerInfoResponse {
    name: string,
    description: string,
    time: string,
    status: enums.VolStatus,
    type: enums.VolType,
    reward: number,
    signable: boolean,
    joiners: SingleUserWithoutAuth[],
    holder: number,
    holderName: string
}

export interface SearchNotices {
    sender: number,
    user: number,
    cls: number,
    school: number
}

export interface NoticeBody {
    title: string,
    content: string,
    deadtime: string
}

export interface Notice extends NoticeBody {
    targets: number[]
}

export interface Report {
    report: string
}

export interface Signup {
    students: number[]
}

export interface SearchThoughts {
    cls: number,
    status: enums.ThoughtStatus,
    student: number,
    volunteer: number
}

export interface SingleThought {
    volId: number,
    stuId: number,
    status: enums.ThoughtStatus,
    stuName: string,
    volName: string
}

export interface Thought {
    thought: string,
    pictures: string[]
}

export interface Login {
    id: number,
    pwd: string
}

export interface SearchUsers {
    name: string,
    cls: number,
    auth: number
}

export interface ModPwd {
    old: string,
    neo: string
}

export interface User {
    name: string,
    cls: number,
    auth: number
}

export interface OneUser extends User {
    id: number
}

export interface Users {
    users: OneUser[]
}

export interface ClassVol {
    id: number,
    max: number
}

export interface SearchVolunteers {
    holder: number,
    student: number,
    cls: number,
    name: string,
    status: enums.VolStatus
}

export interface Volunteer {
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number,
    classes: ClassVol[]
}

export interface Repulse {
    reason: string
}

