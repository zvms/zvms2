import { Categ } from "@/apis/types/enums";
import { defineStore } from "pinia";

export const useInfoStore = defineStore("info", {
  state: () => {
    return {
      userId: NaN,
      username: "",
      permission: Categ.None,
      classId: NaN,
      className: "",
      token: "",
    };
  },
  persist: {
    enabled: true,
    strategies: [
      {
        storage: sessionStorage,
        key: "zvms/v2/info",
      },
    ],
  },
});
