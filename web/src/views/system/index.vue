<template>
  <v-tabs v-model="tab">
    <v-tab v-for="t in tabs" :value="t.id"> {{ t.name }} </v-tab>
  </v-tabs>
  <v-window v-model="tab" style="font-size: larger">
    <v-window-item v-for="t in tabs" :value="t.id">
      <component :is="t.component" />
    </v-window-item>
  </v-window>
</template>

<script lang="ts">
import ServerCtrl from "./server-ctrl.vue";
import Ttyd from "./ttyd.vue";
import VSCode from "./vscode.vue";
import PreviewPort from "./preview-port.vue";
import VConsole from "vconsole";

export default {
  name: "management",
  data() {
    return {
      tab: "server-ctrl", // default tab
    };
  },
  mounted() {
    new VConsole();
  },
  computed: {
    tabs() {
      return [
        {
          name: "服务器",
          id: "server-ctrl",
          component: ServerCtrl,
        },
        {
          name: "TTYD",
          id: "ttyd",
          component: Ttyd,
        },
        {
          name: "VS Code",
          id: "vscode",
          component: VSCode,
        },
        {
          name: "preview port",
          id: "preview-port",
          component: PreviewPort
        }
      ];
    },
  },
};
</script>
