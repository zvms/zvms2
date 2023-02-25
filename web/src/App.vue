<template>
  <v-app class="overflow-y-hidden" full-height>
    <v-theme-provider theme="light">
      <v-navigation-drawer app permanent style="width: 9em">
        <v-list nav dense class="py-0">
          <v-list-item line="two" class="px-0">
            <v-list-item tile class="w-75">
              <img src="./assets/logo.png" />
            </v-list-item>
            <v-list-item>
              <v-list-item-title>义工管理系统</v-list-item-title>
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
            <v-list-item icon>
              <v-icon :icon="item.icon"></v-icon>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
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
