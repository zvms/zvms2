import { v1 as uuid } from "uuid";

const DEVICE_UID_PATH = "zvms/v2/device/uid";

export function getDeviceUID(): string {
  let uid = localStorage.getItem(DEVICE_UID_PATH);
  if (uid === null) {
    uid = uuid();
    localStorage.setItem(DEVICE_UID_PATH, uid);
  }
  return uid;
}

const DEVICE_ASSOC_USERS_PATH = "zvms/v2/device/assoc_users";

export function getAssocUsers() {
  return new Set(
    localStorage.getItem(DEVICE_ASSOC_USERS_PATH)?.split(",") ?? []
  );
}

export function getAssocUsersList() {
  return [...getAssocUsers()];
}

export function addAssocUser(userId: number) {
  const au = getAssocUsers();
  au.add(userId + "");
  localStorage.setItem(DEVICE_ASSOC_USERS_PATH, [...au].join(","));
}

const DEVICE_LATEST_USER_PATH = "zvms/v2/device/latest_user";

export function getLatestUser() {
  return localStorage.getItem(DEVICE_LATEST_USER_PATH);
}

export function setLatestUser(userId: string) {
  localStorage.setItem(DEVICE_LATEST_USER_PATH, userId);
}
