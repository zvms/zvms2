<template>
  <v-btn small @click="restart">Restart ttyd</v-btn>
  <iframe :key="key" class="ttyd" :src="`http://${serverIP}:7681`"></iframe>
</template>
<script lang="ts">
import { fApi } from "@/apis";
import { serverIP } from "@/plugins/axios";
import { toasts } from "@/utils/dialogs";
export default {
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
  },
};
</script>
<style scoped>
.ttyd {
  --scale: 1.22;
  position: absolute;
  width: calc(85% / var(--scale));
  height: calc(90% / var(--scale));
  overflow-y: scroll;
  transform: scale(var(--scale));
  transform-origin: left top;
}
</style>
