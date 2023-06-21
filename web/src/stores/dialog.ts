import { defineStore } from "pinia";

export interface DialogRecord {
  title: string;
  message: string;
  resolve: (value: boolean) => void;
}

export const useDialogStore = defineStore("dialog", {
  state: () => {
    return {
      dialog: null as null | DialogRecord,
    };
  },
  actions: {
    confirm(title: string, message: string = ""): Promise<boolean> {
      const promise = new Promise<boolean>((resolve, _reject) => {
        this.dialog = {
          title,
          message,
          resolve: (v) => {
            this.dialog = null;
            resolve(v);
          },
        };
      });
      return promise;
    },
  },
});
