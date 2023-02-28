import { defineStore } from "pinia";

export const useHeartbeatStore = defineStore("heartbeat", {
  state: () => {
    return {
      intervalId: NaN,
    };
  },
});
