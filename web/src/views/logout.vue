<template>
  <v-card>
    <v-card-title>正在登出...</v-card-title>
  </v-card>
</template>

<script lang="ts">
import { fApi } from "@/apis";
import router from "@/router";
import { useInfoStore, useLastseenvolStore } from "@/stores";
import { applyNavItems } from "@/utils/nav";

export default {
  name: "logout",
  async mounted() {
    fApi.logout()(() => {
      useInfoStore().$reset();
      useLastseenvolStore().$reset();
      applyNavItems();
      router.push("/login");
    });
  },
};
</script>
