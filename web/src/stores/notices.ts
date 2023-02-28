import type { SingleNotice } from "@/apis";
import { defineStore } from "pinia";

export const useNoticesStore = defineStore("notices", {
  state: () => {
    return {
      notices: [
        {
          id: 1,
          title: "TITLE",
          content: "CONTENT",
          sender: 1,
          deadtime: "111/111/111",
          senderName: "1",
        },
      ] as SingleNotice[],
    };
  },
});
