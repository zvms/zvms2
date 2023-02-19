<template>
  <v-app
    class="md overflow-y-hidden"
    full-height
  >
    <v-navigation-drawer
      app
      permanent
      style="backdrop-filter: blur(10px)"
    >
      <v-list nav dense class="py-0">
        <v-list-item line="two" class="px-0">
          <v-list-item tile >
            <img src="./assets/logo.png" />
          </v-list-item>
          <v-list-item>
            <v-list-item-title>义工管理系统</v-list-item-title>
            <v-list-item-subtitle>v1.3.2</v-list-item-subtitle>
          </v-list-item>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item
          v-for="item in drawerStore.items"
          :key="item.title"
          :to="item.to"
          link
        >
          <v-list-item icon>
            <v-icon :icon="item.icon"></v-icon>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-3">
          <v-progress-circular
            color="black"
            indeterminate
            v-show="loadingStore.isLoading"
          ></v-progress-circular>
        </div>
      </template>
    </v-navigation-drawer>
    <v-main>
      <v-container>
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { applyNavItems } from "@/utils/nav";
import {
  useDrawerStore,
  useLoadingStore,
} from "@/stores";
import { mapStores } from "pinia";
import router from "./router";

export default {
  name: "App",
  data() {
    return {
      activeBtn: 1,
      drawer: true,
      phone: false,
      currentVol: undefined,
    };
  },
  mounted() {
    applyNavItems();
  },
  computed: {
    ...mapStores(
      useDrawerStore,
      useLoadingStore
    ),
  },
};
</script>
