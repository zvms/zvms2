<template>
  <v-container>
    <v-btn class="ma-30" @click="restartBackend">
      <span style="font-size: x-large"> Restart backend </span>
    </v-btn>
  </v-container>
</template>
<script lang="ts">
import { fApi } from "@/apis";
import { confirm } from "@/utils/dialogs";
export default {
  name: "server-ctrl",
  data() {
    return {};
  },
  methods: {
    async restartBackend() {
      if (await confirm("确定重启？")) {
        if (await confirm("确定重启*2 ？")) {
          if (await confirm("确定重启*3 ？")) {
            fApi.restart()();
          }
        }
      }
    },
  },
};
</script>
