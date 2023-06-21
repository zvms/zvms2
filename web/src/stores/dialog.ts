import { defineStore } from "pinia";

export enum DialogType {
  Confirm,
  Success,
  Error,
  Warn,
  Info,
}

export type DialogRecord = {
  key: number;
} & (
  | {
      type: DialogType.Confirm;
      title: string;
      message: string;
      resolve: (value: boolean) => void;
    }
  | {
      type:
        | DialogType.Success
        | DialogType.Error
        | DialogType.Warn
        | DialogType.Info;
      message: string;
    }
);

export const useDialogStore = defineStore("dialog", {
  state: () => {
    return {
      dialog: null as null | DialogRecord,
    };
  },
  actions: {
    confirm(title: string, message: string): Promise<boolean> {
      const promise = new Promise<boolean>((resolve, reject) => {
        this.dialog = {
          type: DialogType.Confirm,
          key: Date.now(),
          title,
          message,
          resolve,
        };
      });
      return promise;
    },
    success(message: string) {
      this.dialog = {
        type: DialogType.Success,
        key: Date.now(),
        message,
      };
      this.registerTimeout(this.dialog.key, 3000);
    },
    error(message: string) {
      this.dialog = {
        type: DialogType.Error,
        key: Date.now(),
        message,
      };
      this.registerTimeout(this.dialog.key, 5000);
    },
    warn(message: string) {
      this.dialog = {
        type: DialogType.Warn,
        key: Date.now(),
        message,
      };
      this.registerTimeout(this.dialog.key, 3000);
    },
    info(message: string) {
      this.dialog = {
        type: DialogType.Info,
        key: Date.now(),
        message,
      };
      this.registerTimeout(this.dialog.key, 3000);
    },
    registerTimeout(key: number, timeout: number) {
      setTimeout(() => {
        this.close(key);
      }, timeout);
    },
    close(key: number) {
      if (this.dialog?.key === key) {
        this.dialog = null;
      }
    },
  },
});
