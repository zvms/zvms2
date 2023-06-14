import { defineStore } from "pinia";
import { NoRetryTime, MaxLoadingTime } from "@/utils/calc";

export interface LoadingRecord {
  symbol: symbol;
  start: number;
}

export const useLoadingStore = defineStore("loading", {
  state: () => {
    return {
      loadings: [] as LoadingRecord[],
      noretryStart: NaN, // start time
    };
  },
  actions: {
    incLoading(): Symbol {
      const symbol = Symbol();
      this.loadings.push({
        symbol,
        start: Date.now()
      });
      return symbol;
    },
    decLoading(symbol: Symbol) {
      const idx = this.loadings.findIndex((v) => v.symbol === symbol)
      if (idx === -1) {
        throw new Error("Cannot decrease loadingNum: no such symbol");
      }
      this.loadings.splice(idx, 1);
    },
    calcIsLoading() { // This can't be a getter, because it uses current time and may modify `this.loadings`
      const now = Date.now()
      this.loadings = this.loadings.filter(
        v => v.start + MaxLoadingTime > now
      );
      return this.loadings.length > 0;
    }
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

export function isNoRetry(
  loadingStore: ReturnType<typeof useLoadingStore>
): boolean {
  return (
    Number.isFinite(loadingStore.noretryStart) &&
    loadingStore.noretryStart + NoRetryTime >= Date.now()
  );
}
