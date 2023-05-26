<template>
  <v-btn @click="restart">Restart ttyd</v-btn>
  <v-btn @click="reload">Reload iframe</v-btn>
  <br />
  <iframe :key="key" class="ttyd" :src="`http://${serverIP}:7681`"></iframe>
</template>
<script lang="ts">
import { fApi } from "@/apis";
import { serverIP } from "@/plugins/axios";
export default {
  name: "ttyd",
  data() {
    return {
      serverIP,
      key: 0,
    };
  },
  methods: {
    restart() {
      fApi.restartTtyd()();
    },
    reload() {
      this.key++;
    },
  },
};
</script>
<style scoped>
.ttyd {
  --scale: 1.22;
  z-index: 1000;
  position: fixed;
  width: calc(85% / var(--scale));
  height: calc(95% / var(--scale) - 60px);
  overflow-y: scroll;
  transform: scale(var(--scale));
  transform-origin: left top;
}
</style>
