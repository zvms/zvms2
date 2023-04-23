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
        to: route.path,
        info: route.meta.nav,
      });
  }
  return items;
}

export function applyNavItems() {
  return (useNavStore().items = getNavItems(
    useInfoStore().permission || Categ.None
  ));
}
