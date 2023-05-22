import { v1 as uuid } from "uuid";

const DEVICE_KEY_PATH = "zvms.v2.device.key";

export function getDeviceKey(): string {
  let dk = localStorage.getItem(DEVICE_KEY_PATH);
  if (dk === null) {
    dk = uuid();
    localStorage.setItem(DEVICE_KEY_PATH, dk);
  }
  return dk;
}

const DEVICE_ASSOC_USERS_PATH = "zvms.v2.device.assoc_users";

export function getAssocUsers() {
  return new Set(
    ...(localStorage.getItem(DEVICE_ASSOC_USERS_PATH)?.split(",") ?? [])
  );
}

export function getAssocUsersList() {
  return [...getAssocUsers()];
}

export function addAssocUsers(userId: string) {
  const au = getAssocUsers();
  au.add(userId);
  localStorage.setItem(DEVICE_ASSOC_USERS_PATH, [...au].join(","));
}
