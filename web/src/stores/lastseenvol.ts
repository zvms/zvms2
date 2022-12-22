import { defineStore } from 'pinia'

export const useLastseenvolStore = defineStore('lastseenvol', {
  state: () => {
    return {
      lastseenvol: [] as any[]
    }
  }
})