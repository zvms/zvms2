<template>
  <iframe
    style="width: 100%; height: 650px"
    :src="`http://${serverIP}:7681`"
  ></iframe>
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
