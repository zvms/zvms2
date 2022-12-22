import { defineStore } from 'pinia'

export const useNoticesStore = defineStore('notices', {
  state: () => {
    return {
      notices: []
    }
  }
})