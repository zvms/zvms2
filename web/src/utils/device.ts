import { v1 as uuid } from "uuid";
import { toasts } from "@/plugins/toastification";

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
  try{
    const raw = localStorage.getItem(DEVICE_ASSOC_USERS_PATH);
    if(!raw){
      return {};
    }
    let parsed: object;
    if(raw[0]!=="{"){ // Adapt to the old storage format. Can be removed months later.
      parsed = {};
      for(const id of raw.split(",")){
        parsed[id] = 1;
      }
      localStorage.setItem(DEVICE_ASSOC_USERS_PATH, JSON.stringify(parsed));
    }else{
      parsed = JSON.parse(raw);
    }
    return parsed;
  }catch(e:any){
    toasts.warning(`Error: ${e} when getting associated users.`);
    localStorage.setItem(DEVICE_ASSOC_USERS_PATH, "");
  }
}

export function addAssocUser(userId: number) {
  const au = getAssocUsers();
  au[userId] = 1 + (au[userId] ?? 0);
  localStorage.setItem(DEVICE_ASSOC_USERS_PATH, JSON.stringify(au));
}

const DEVICE_LATEST_USER_PATH = "zvms/v2/device/latest_user";

export function getLatestUser() {
  return localStorage.getItem(DEVICE_LATEST_USER_PATH);
}

export function setLatestUser(userId: string) {
  localStorage.setItem(DEVICE_LATEST_USER_PATH, userId);
}
