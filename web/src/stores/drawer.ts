import { getNavItems } from '@/utils/nav'
import { permissionTypes } from '@/utils/permissions'
import { defineStore } from 'pinia'

export const useDrawerStore = defineStore('drawer', {
  state: () => {
    return {
      items: getNavItems(permissionTypes.none)
    }
  }
})