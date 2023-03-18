import { getNavItems } from "@/utils/nav";
import { Categ } from "@/apis/types/enums";
import { defineStore } from "pinia";

export const useNavStore = defineStore("nav", {
  state: () => {
    return {
      items: getNavItems(Categ.None),
    };
  },
});
