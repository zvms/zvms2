import { getNavItems } from "@/utils/nav";
import { permissionTypes } from "@/utils/permissions";
import { defineStore } from "pinia";

export const useNavStore = defineStore("nav", {
  state: () => {
    return {
      items: getNavItems(permissionTypes.none),
    };
  },
});
