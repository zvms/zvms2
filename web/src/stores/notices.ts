import type { SingleNotice } from "@/apis";
import { defineStore } from "pinia";

export const useNoticesStore = defineStore("notices", {
  state: () => {
    return {
      notices: [] as SingleNotice[],
    };
  },
});
