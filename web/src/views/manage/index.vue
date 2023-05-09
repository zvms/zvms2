<template>
  <v-card>
    <v-card-title> 后台管理 </v-card-title>
    <v-card-text>
      <v-tabs v-model="tab">
        <v-tab value="modify-pwd"> 修改他人密码 </v-tab>
        <v-tab value="import-time"> 导入时长 </v-tab>
        <v-tab value="view-report"> 查看反馈 </v-tab>
      </v-tabs>
      <v-window v-model="tab" style="font-size:larger">
        <v-window-item value="modify-pwd">
          <modify-pwd />
        </v-window-item>
        <v-window-item value="import-time">
          <import-time />
        </v-window-item>
        <v-window-item value="view-report">
          <view-report />
        </v-window-item>
      </v-window>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import ModifyPwd from "./modify-pwd.vue";
import ImportTime from "./import-time.vue";
import ViewReport from "./view-report.vue";

export default {
  name: "management",
  components: {
    ModifyPwd,
    ImportTime,
    ViewReport
  },
  data() {
    return {
      tab: "modify-pwd", // default tab
    };
  },
};
</script>
