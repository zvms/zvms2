import CryptoJS from "crypto-js";

export function md5(str: string): string {
  return CryptoJS.MD5(str).toString();
}
