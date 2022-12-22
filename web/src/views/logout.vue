<template>
  <v-card>
    <v-card-title>正在登出...</v-card-title>
  </v-card>
</template>

<script lang="ts">
import { logout } from "../apis";

export default {
  name: "logout",
  async mounted() {
    await logout();
  }
};
</script>>