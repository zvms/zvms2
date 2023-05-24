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
  },
  persist: {
    enabled: true,
    strategies: [
      {
        storage: localStorage,
        key: "zvms/v2/noretry_start",
        paths: ["noretryStart"],
      },
    ],
  },
});

export function mapIsLoading() {
  return mapState(useLoadingStore, ["isLoading"]);
}

export function isNoRetry(
  loadingStore: ReturnType<typeof useLoadingStore>
): boolean {
  return (
    Number.isFinite(loadingStore.noretryStart) &&
    loadingStore.noretryStart + 1000 * 60 * 5 >= Date.now()
  );
}
