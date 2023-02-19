<template>
  <v-app
    style="
      background-size: cover;
      background-attachment: fixed;
      overflow-y: hidden;
    "
  >
    <v-navigation-drawer
      app
      permanent
      style="backdrop-filter: blur(10px)"
    >
      <v-list nav dense class="py-0">
        <v-list-item line="two" class="px-0">
          <v-list-item tile>
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
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-3">
          <v-progress-circular
            color="white"
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

<style>
::-webkit-scrollbar {
  width: 0px;
  height: 4px;
}

::-webkit-scrollbar-button {
  width: 0px;
  height: 0;
}

#drag {
  padding: 0;
  margin: 0;
}
</style>

<script lang="ts">
//import { RouterLink, RouterView } from 'vue-router'
import { fApi } from "@/apis";
import { permissionTypes } from "@/utils/permissions.js";
import { applyNavItems } from "@/utils/nav";
import {
  useNoticesStore,
  useInfoStore,
  useLastseenvolStore,
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
    router.push("/login")
    applyNavItems();
  },
  methods: {
   
  },

  computed: {
    ...mapStores(
      useNoticesStore,
      useInfoStore,
      useLastseenvolStore,
      useDrawerStore,
      useLoadingStore
    ),
  },
};
</script>
