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
    confirm(title: string, message: string = ""): Promise<boolean> {
      const promise = new Promise<boolean>((resolve, reject) => {
        const key = Date.now();
        this.dialog = {
          type: DialogType.Confirm,
          key,
          title,
          message,
          resolve: (v) => {
            this.close(key);
            resolve(v);
          },
        };
      });
      return promise;
    },
    success(message: string) {
      const key = Date.now();
      this.dialog = {
        type: DialogType.Success,
        key,
        message,
      };
      this.registerTimeout(key, 3000);
    },
    error(message: string) {
      const key = Date.now();
      this.dialog = {
        type: DialogType.Error,
        key,
        message,
      };
      this.registerTimeout(key, 5000);
    },
    warn(message: string) {
      const key = Date.now();
      this.dialog = {
        type: DialogType.Warn,
        key,
        message,
      };
      this.registerTimeout(key, 3000);
    },
    info(message: string) {
      const key = Date.now();
      this.dialog = {
        type: DialogType.Info,
        key,
        message,
      };
      this.registerTimeout(key, 3000);
    },
    validateForm(isFormValid: boolean) {
      if (!isFormValid) {
        this.error("请检查表单是否填写正确");
      }
      return isFormValid;
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
