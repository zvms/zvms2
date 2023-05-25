import * as enums from "./enums";

export interface Class{
    name: string
}
export interface SingleClass{
    id: number,
    name: string
}
export interface SingleUserWithoutAuth{
    id: number,
    name: string
}
export interface SingleUser extends SingleUserWithoutAuth{
    auth: number
}
export type ListClassesResponse = Array<SingleClass>
export interface ClassInfoResponse{
    name: string,
    students: Array<SingleUser>,
    teachers: Array<SingleUser>
}
export interface ClassStudentNum{
    num: number
}
export interface UserLoginResponse{
    token: string,
    id: number
}
export type SearchUsersResponse = Array<SingleUser>
export interface UserBasicInfoResponse{
    clsName: string,
    userName: string
}
export interface UserInfoResponse{
    name: string,
    school_id: number,
    cls: number,
    auth: number,
    clsName: string
}
export interface PictureResponse{
    hash: string,
    type: string
}
export interface ThoughtInfoResponse{
    status: enums.ThoughtStatus,
    thought: string,
    pics: Array<PictureResponse>,
    reward: number,
    everRepulsed: boolean,
    reason: string
}
export interface StudentThoughtsResponse{
    accepted: Array<ThoughtInfoResponse>,
    unsubmitted: Array<ThoughtInfoResponse>,
    draft: Array<ThoughtInfoResponse>,
    unaudited: Array<ThoughtInfoResponse>
}
export interface StudentStatResponse{
    inside: number,
    outside: number,
    large: number
}
export interface SingleNotice{
    id: number,
    title: string,
    content: string,
    sender: number,
    sendtime: string,
    deadtime: string,
    senderName: string
}
export type SearchNoticesResponse = Array<SingleNotice>
export interface SingleSignup{
    volId: number,
    volName: string,
    stuId: number,
    stuName: string
}
export type ListSignupResponse = Array<SingleSignup>
export interface SingleVolunteer{
    id: number,
    name: string,
    time: string,
    status: number,
    signable: boolean,
    joiners: Array<SingleUserWithoutAuth>,
    holderName: string
}
export type SearchVolunteersResponse = Array<SingleVolunteer>
export interface SearchNotices{
    sender?: number,
    receiver?: number,
    cls?: number,
    school?: number
}
export interface NoticeBody{
    title: string,
    content: string,
    deadtime: string
}
export interface Notice extends NoticeBody{
    targets: Array<number>,
    anonymous: boolean
}
export interface SchoolNotice extends NoticeBody{
    anonymous: boolean
}
export interface Report{
    report: string
}
export interface SingleReport{
    content: string,
    reporter: number,
    reporterName: string,
    time: string
}
export type FetchReportsResponse = Array<SingleReport>
export interface Signup{
    students: Array<number>
}
export interface SearchThoughts{
    cls?: number,
    status?: enums.ThoughtStatus,
    student?: number,
    volunteer?: number
}
export interface SearchStudentThoughts{
    status?: enums.ThoughtStatus
}
export interface SingleThought{
    volId: number,
    stuId: number,
    status: enums.ThoughtStatus,
    stuName: string,
    volName: string,
    volTime: string
}
export type SearchThoughtsResponse = Array<SingleThought>
export interface BasePictrure{
    type: string
}
export interface ExistedPicture extends BasePictrure{
    hash: string,
    type: string
}
export interface Base64Picture extends BasePictrure{
    base64: string,
    type: string
}
export type Picture = ExistedPicture | Base64Picture
export interface Thought{
    thought: string,
    pictures: Array<ExistedPicture | Base64Picture>
}
export interface Login{
    id: string,
    pwd: string,
    devideId: string
}
export interface SearchUsers{
    name?: string,
    cls?: number,
    auth?: number
}
export interface ModPwd{
    old: string,
    neo: string
}
export interface User{
    name: string,
    cls: number,
    auth: number
}
export interface OneUser extends User{
    id: number
}
export interface Users{
    users: Array<OneUser>
}
export interface ClassVol{
    id: number,
    max: number
}
export interface ClassVolWithName extends ClassVol{
    name: string
}
export interface ListVolunteers{
    cls?: number
}
export interface SearchVolunteers{
    holder?: number,
    student?: number,
    cls?: number,
    name?: string,
    status?: enums.VolStatus,
    signable?: boolean
}
export interface VolunteerBody{
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number
}
export interface Volunteer extends VolunteerBody{
    classes: Array<ClassVol>
}
export interface VolunteerInfoResponse{
    name: string,
    description: string,
    time: string,
    status: enums.VolStatus,
    type: enums.VolType,
    reward: number,
    signable: boolean,
    classes: Array<ClassVolWithName>,
    joiners: Array<SingleUserWithoutAuth>,
    holder: number,
    holderName: string
}
export interface AppointedVolunteer extends VolunteerBody{
    joiners: Array<number>
}
export interface Repulse{
    reason: string
}
export interface Accept{
    reward: number
}
export interface FetchPicture{
    url: string
}
export interface PublicNoticeNotNone{
    title: string,
    content: string
}
export type PublicNotice = PublicNoticeNotNone | null
export interface ModOthersPwd{
    pwd: string
}
export interface SpecialVolunteer{
    name: string,
    type: enums.VolType,
    reward: number,
    joiners: Array<number>
}
