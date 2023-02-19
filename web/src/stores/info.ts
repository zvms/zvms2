import { permissionTypes } from "@/utils/permissions";
import { defineStore } from "pinia";

export const useInfoStore = defineStore("info", {
  state: () => {
    return {
      userId:NaN,
      username: "",
      permission: permissionTypes.none as permissionTypes,
      classId: NaN,
      className: "",
      token: "",
    };
  },
  persist: {
    enabled: true,
  },
});
