import { useNavStore, useInfoStore } from "@/stores";
import { Categ } from "@/apis/types/enums";
import router, { type NavItemInfo } from "@/router";

export function getNavItems(permission: Categ) {
  const items: {
    to: string;
    info: NavItemInfo;
  }[] = [];

  for (const route of router.getRoutes()) {
    if (route.meta.nav && route.meta.authed(permission))
      items.push({
        to: route.meta.nav.specifiedPath ?? route.path,
        info: route.meta.nav,
      });
  }
  return items.sort((v1, v2) => {
    return v1.info.priority - v2.info.priority;
  });
}

export function applyNavItems() {
  return (useNavStore().items = getNavItems(
    useInfoStore().permission || Categ.None
  ));
}
