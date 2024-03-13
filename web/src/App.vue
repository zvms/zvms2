<template>
  <VApp full-height>
    <VThemeProvider theme="light">
      <VNavigationDrawer
        app
        permanent
        style="width: 7em; max-width: 17%"
        touchless
      >
        <VList nav dense class="py-0">
          <VListItem line="one" class="px-0">
            <!-- <v-list-item tile class="w-50">
              <img src="./assets/logo.png" />
            </v-list-item> -->
            <VListItem class="pt-4">
              <VListItemTitle style="font-size: medium">
                <span
                  style="color: rgb(var(--v-theme-color2)); font-size: larger"
                  class="py-2 pt-4"
                >
                  镇海中学
                </span>
                <br />
                义工管理系统
              </VListItemTitle>
              <VListItemSubtitle>{{ VERSION }}</VListItemSubtitle>
            </VListItem>
          </VListItem>
          <VDivider></VDivider>
          <VListItem
            v-for="item in navStore.items"
            :key="item.info.title"
            :to="item.to"
            link
          >
            <VIcon :icon="item.info.icon" small></VIcon>
            <VListItemTitle>{{ item.info.title }}</VListItemTitle>
          </VListItem>
        </VList>
        <template v-slot:append>
          <div class="pa-3 text-center pb-10">
            <VProgressCircular
              color="primary"
              indeterminate
              v-show="loadingStore.isLoading"
            />
          </div>
        </template>
      </VNavigationDrawer>
      <VMain>
        <VContainer class="pl-1 pb-0 pt-2 pr-5">
          <RouterView />
        </VContainer>
      </VMain>
    </VThemeProvider>
    <div id="prevent-click-hover" v-if="loadingStore.isLoading"></div>
    <VCard v-if="dialogStore.dialog" style="position: fixed; left: 30%; width: 40%; top:30%; height: 30%">
      <VCardTitle>{{ dialogStore.dialog!.title }}</VCardTitle>
      <VCardText>
        {{ dialogStore.dialog!.message }}
        <br/>
      </VCardText>
      <VCardActions>
        <VBtn @click="dialogStore.dialog!.resolve(true)">确认</VBtn>
        <VBtn @click="dialogStore.dialog!.resolve(false)">取消</VBtn>
      </VCardActions>
    </VCard>
  </VApp>
</template>

<script lang="ts">
import { applyNavItems } from "@/utils/nav";
import { useNavStore, useLoadingStore, useDialogStore } from "@/stores";
import { mapStores } from "pinia";
import { VERSION } from "@/utils/metadata";

export default {
  name: "App",
  data() {
    return {
      VERSION,
    };
  },
  beforeMount() {
    applyNavItems();
  },
  computed: {
    ...mapStores(useNavStore, useLoadingStore, useDialogStore),
  },
};
</script>
<style scoped>
#prevent-click-hover {
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: 10000;
  color: transparent;
}
</style>
