import { defineStore, mapState } from "pinia";

export const useLoadingStore = defineStore("loading", {
  state: () => {
    return {
      loadingNum: 0,
      noretryStart: NaN, // start time
    };
  },
  actions: {
    incLoading() {
      this.loadingNum++;
    },
    decLoading() {
      if (this.loadingNum <= 0) {
        throw new Error("Cannot decrease loadingNum: loadingNum<=0");
      }
      this.loadingNum--;
    },
  },
  getters: {
    isLoading: (state) => state.loadingNum > 0,
    noretry: (state) =>
      isFinite(state.noretryStart) &&
      state.noretryStart + 1000 * 60 * 5 >= Date.now(),
  },
  persist: {
    enabled: true,
    strategies: [
      {
        storage: localStorage,
        key: "zvms/v2/noretryStart",
        paths: ["noretryStart"],
      },
    ],
  },
});

export function mapIsLoading() {
  return mapState(useLoadingStore, ["isLoading"]);
}
