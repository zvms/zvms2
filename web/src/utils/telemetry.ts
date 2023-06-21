import { useDialogStore } from "@/stores";

export function registerTelemetry() {
  window.addEventListener("error", (ev) => {
    useDialogStore().error(`前端出错啦！请刷新一下。
              ${ev.filename}第${ev.lineno}行第${ev.colno}列：${ev.error}`);
    return false;
  });

  const consoleErrorBackup = console.error;
  console.error = (...ev) => {
    useDialogStore().error(
      `前端出错啦！请刷新一下。${ev.map((v) => v + "").join(", ")}`
    );
    consoleErrorBackup(...ev);
  };
}
