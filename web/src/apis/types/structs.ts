import * as enums from "./enums.js";
export interface Class {
  name: string;
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
  type: number;
  targets: Array<number>;
}
export interface Report {
  content: string;
}
export interface Signup {
  stuList: Array<number>;
}
export interface Thought {
  content: string;
  pictures: Array<string>;
}
export interface Login {
  id: number;
  pwd: string;
}
export interface ModPwd {
  old: string;
  new: string;
}
export interface ChangeClass {
  cls: number;
}
export interface VolunteerRecordClass {
  id: number;
  max: number;
}
export interface UserOfUsers {
  id: number;
  name: string;
  cls: number;
  auth: number;
  pwd: string;
}
export interface Users {
  users: Array<UserOfUsers>;
}
export interface User {
  name: string;
  cls: number;
  auth: number;
}
export interface VolunteerRecord {
  name: string;
  description: string;
  time: string;
  type: number;
  reward: number;
  classes: Array<VolunteerRecordClass>;
}
