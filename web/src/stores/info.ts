import { permissionTypes } from "@/utils/permissions";
import { defineStore } from "pinia";

export const useInfoStore = defineStore("info", {
  state: () => {
    return {
      username: "",
      permission: permissionTypes.none as permissionTypes,
      class: 0,
      classname: "",
      token: "",
    };
  },
  persist: {
    enabled: true,
  },
});
