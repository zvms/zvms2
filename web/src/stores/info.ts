import { permissionTypes } from '@/utils/permissions'
import { defineStore } from 'pinia'

export const useInfoStore = defineStore('info', {
  state: () => {
    return {
      username: "",
      permission: permissionTypes.none,
      class: "",
      classname: "",
      token: ""
    }
  },
  persist: {
    enabled: true,
  }
})