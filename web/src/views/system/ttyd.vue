<template>
  <iframe class="ttyd" :src="`http://${serverIP}:7681`"></iframe>
</template>
<script lang="ts">
import { serverIP } from "@/plugins/axios";
export default {
  data() {
    return {
      serverIP,
    };
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
