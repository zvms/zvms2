<template>
  <v-text-field v-model.number="port" />
  <a :href="url">
    <v-btn color="primary" class="submit">PREVIEW</v-btn>
  </a>
</template>
<script lang="ts">
import { serverIP } from "@/plugins/axios";

export default {
  name: "preview-port",
  data() {
    return {
      port: 5173,
    };
  },
  computed: {
    url() {
      return `http://${serverIP}:${this.port}`;
    },
  },
};
</script>
