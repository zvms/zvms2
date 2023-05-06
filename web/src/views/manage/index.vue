<template>
  
  <v-tabs v-model="tab">
    <v-tab value="modify-pwd"> 修改他人密码 </v-tab>
  </v-tabs>
  <v-window v-model="tab">
    <v-window-item value="modify-pwd">
      <modify-pwd />
    </v-window-item>
  </v-window>
</template>

<script lang="ts">
import ModifyPwd from "./modify_pwd.vue";

export default {
  name: "management",
  components: {
    ModifyPwd,
  },
  data() {
    return {
      tab: "modify-pwd",
    };
  },
};
</script>
