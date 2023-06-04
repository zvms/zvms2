import { toasts } from "@/utils/dialogs";

export function registerTelemetry() {
  window.addEventListener("error", (ev) => {
    toasts.error(`前端出错啦！请刷新一下。
              ${ev.filename}第${ev.lineno}行第${ev.colno}列：${ev.error}`);
    return false;
  });

  const consoleErrorBackup = console.error;
  console.error = (...ev) => {
    toasts.error(`前端出错啦！请刷新一下。${ev.map((v) => v + "").join(", ")}`);
    consoleErrorBackup(...ev);
  };
}
