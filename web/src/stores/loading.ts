import { defineStore } from "pinia";
import { NoRetryTime, MaxLoadingTime } from "@/utils/calc";

export interface LoadingRecord {
  symbol: symbol;
  start: number;
  timer: number;
}

export const useLoadingStore = defineStore("loading", {
  state: () => {
    return {
      loadings: [] as LoadingRecord[],
      noRetryStart: NaN, // start time
      timer: NaN,
    };
  },
  actions: {
    incLoading(): Symbol {
      const symbol = Symbol();
      this.loadings.push({
        symbol,
        start: Date.now(),
        timer: setTimeout(() => {
          this.decLoading(symbol, true);
        }, MaxLoadingTime)
      });
      loadingStateChangeCallback(true);
      return symbol;
    },
    decLoading(symbol: Symbol, timeout = false) {
      const idx = this.loadings.findIndex((v) => v.symbol === symbol)
      if (idx === -1) {
        throw new Error("Cannot decrease loadingNum: no such symbol");
      }
      if (!timeout) {
        clearTimeout(this.loadings[idx].timer);
      }
      this.loadings.splice(idx, 1);
    }
  },
  getters: {
    isLoading(): boolean{
      return this.loadings.length > 0;
    }
  },
  persist: {
    enabled: true,
    strategies: [
      {
        storage: localStorage,
        key: "zvms/v2/noRetry_start",
        paths: ["noRetryStart"],
      },
    ],
  },
});

export function isNoRetry(
  loadingStore: ReturnType<typeof useLoadingStore>
): boolean {
  return (
    Number.isFinite(loadingStore.noRetryStart) &&
    loadingStore.noRetryStart + NoRetryTime >= Date.now()
  );
}
