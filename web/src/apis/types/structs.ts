import * as enums from "./enums";
export interface Class {
  name: string;
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
