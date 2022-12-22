import { defineStore, mapState } from 'pinia'

export const useLoadingStore = defineStore('loading', {
  state: () => {
    return {
      loadingNum: 0
    }
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
    isLoading: (state) => state.loadingNum > 0
  }
})

export function mapIsLoading(){
  return mapState(useLoadingStore,["isLoading"]);
}