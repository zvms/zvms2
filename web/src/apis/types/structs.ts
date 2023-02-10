import * as enums from "././enums";
export interface Class {
  name: string;
}
export interface SingleClass {
  id: number;
  name: string;
}
export interface SingleUserWithoutAuth {
  id: number;
  name: string;
}
export interface SingleUser {
  id: number;
  name: string;
  auth: number;
}
export type ListClassesResponse = Array<SingleClass>;
export interface ClassInfoResponse {
  name: string;
  students: Array<SingleUser>;
  teachers: Array<SingleUser>;
}
export interface UserLoginResponse {
  token: string;
}
export type SearchUsersResponse = Array<SingleUser>;
export interface UserInfoResponse {
  name: string;
  cls: number;
  auth: number;
  clsName: string;
}
export interface VolunteerTimeResponse {
  inside: number;
  outside: number;
  large: number;
}
export interface SingleNotice {
  id: number;
  title: string;
  content: string;
  sender: number;
  deadtime: string;
  senderName: string;
}
export type SearchNoticesResponse = Array<SingleNotice>;
export interface SingleSignup {
  volId: number;
  volName: string;
  stuId: number;
  stuName: string;
}
export type ListSignupResponse = Array<SingleSignup>;
export interface SingleVolunteer {
  id: number;
  name: string;
  time: string;
  status: number;
}
export type SearchVolunteersResponse = Array<SingleVolunteer>;
export interface VolunteerInfoResponse {
  name: string;
  description: string;
  time: string;
  type: number;
  reward: number;
  joiners: Array<SingleUserWithoutAuth>;
  holder: number;
  holderName: string;
}
export interface SearchNotices {
  sender: number;
  user: number;
  cls: number;
  school: any;
}
export interface NoticeBody {
  title: string;
  content: string;
  deadtime: string;
}
export interface Notice {
  title: string;
  content: string;
  deadtime: string;
  targets: Array<number>;
}
export interface Report {
  report: string;
}
export interface Signup {
  students: Array<number>;
}
export interface SearchThoughts {
  cls: number;
  status: enums.ThoughtStatus;
  student: number;
  Volunteer: number;
}
export interface Thought {
  thought: string;
  pictures: Array<string>;
}
export interface Login {
  id: number;
  pwd: string;
}
export interface SearchUsers {
  name: string;
  cls: number;
  auth: number;
}
export interface ModPwd {
  old: string;
  neo: string;
}
export interface ChangeClass {
  cls: number;
}
export interface User {
  name: string;
  cls: number;
  auth: number;
}
export interface OneUser {
  name: string;
  cls: number;
  auth: number;
  id: number;
}
export interface Users {
  users: Array<OneUser>;
}
export interface ClassVol {
  id: number;
  max: number;
}
export interface SearchVolunteers {
  holder: number;
  student: number;
  cls: number;
  name: string;
  status: enums.VolStatus;
}
export interface Volunteer {
  name: string;
  description: string;
  time: string;
  type: enums.VolType;
  reward: number;
  classes: Array<ClassVol>;
}
export interface Repulse {
  reason: string;
}
