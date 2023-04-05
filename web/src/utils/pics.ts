import axios from "axios";
import CryptoJS from "crypto-js";

const keyTableApiUrl =
  "https://gitee.com/api/v5/repos/zvms/zvms-imagebed/issues/comments/17281159?access_token=bce04e8d78a6e8e5fa514aa96d79d417";

type KeyTable = [short: string, remoteUrl: string][];

async function fetchTable(): Promise<KeyTable> {
  const response = await axios.get(keyTableApiUrl);
  const text = response.data.body as string;
  const table = text
    .split("\n")
    .map((s) => s.split("="))
    .map((ss) => [ss[0].trim(), ss[1].trim()] as [string, string]);
  return table;
}

export async function getPicsById(shortKey: string) {
  const table = await fetchTable();
  return table.filter((s) => s[0] === shortKey).map((s) => s[1]);
}

export function ArrayBufferToWordArray(arrayBuffer: ArrayBuffer | Uint8Array) {
  let u8: Uint8Array;
  if (arrayBuffer instanceof ArrayBuffer)
    u8 = new Uint8Array(arrayBuffer, 0, arrayBuffer.byteLength);
  else u8 = arrayBuffer;
  const len = u8.length;
  const words: any[] = [];
  for (let i = 0; i < len; i += 1) {
    words[i >>> 2] |= (u8[i] & 0xff) << (24 - (i % 4) * 8);
  }
  return CryptoJS.lib.WordArray.create(words, len);
}
