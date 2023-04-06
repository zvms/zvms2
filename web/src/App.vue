<template>
  <v-app class="overflow-y-hidden" full-height>
    <v-theme-provider theme="light">
      <v-navigation-drawer
        app
        permanent
        style="width: 7em; max-width: 17%"
        touchless
      >
        <v-list nav dense class="py-0">
          <v-list-item line="two" class="px-0">
            <!-- <v-list-item tile class="w-50">
              <img src="./assets/logo.png" />
            </v-list-item> -->
            <v-list-item class="pt-5">
              <v-list-item-title style="font-size: medium"
                ><span
                  style="color: rgb(var(--v-theme-color2)); font-size: larger"
                  >镇海中学</span
                ><br />义工管理系统</v-list-item-title
              >
              <v-list-item-subtitle>v2.0.0</v-list-item-subtitle>
            </v-list-item>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item
            v-for="item in navStore.items"
            :key="item.title"
            :to="item.to"
            link
          >
            <v-icon :icon="item.icon" small></v-icon>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
        <template v-slot:append>
          <div class="pa-3 text-center pb-10">
            <v-progress-circular
              color="primary"
              indeterminate
              v-show="loadingStore.isLoading"
            />
          </div>
        </template>
      </v-navigation-drawer>
      <v-main>
        <v-container>
          <RouterView />
        </v-container>
      </v-main>
    </v-theme-provider>
    <div id="prevent-click" v-if="loadingStore.isLoading"></div>
  </v-app>
</template>

<script lang="ts">
import { applyNavItems } from "@/utils/nav";
import { useNavStore, useLoadingStore } from "@/stores";
import { mapStores } from "pinia";

export default {
  name: "App",
  mounted() {
    applyNavItems();
  },
  computed: {
    ...mapStores(useNavStore, useLoadingStore),
  },
};
</script>
<style scoped>
#prevent-click {
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: 10000;
  color: transparent;
}
</style>
