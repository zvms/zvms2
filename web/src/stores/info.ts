import { permissionTypes } from "@/utils/permissions";
import { defineStore } from "pinia";

export const useInfoStore = defineStore("info", {
  state: () => {
    return {
      userId: 111111, //NaN,
      username: "admin", //"",
      permission: 0xfffffff, //permissionTypes.none as permissionTypes,
      classId: 12333, // NaN,
      className: "className", //"",
      token: "",
    };
  },
  persist: {
    enabled: true,
  },
});
