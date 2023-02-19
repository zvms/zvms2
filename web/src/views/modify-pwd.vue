<template>
  <v-container>
    <v-card>
      <v-card-title>修改密码</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="oldPwd"
          label="旧密码"
          type="password"
          prepend-icon="mdi-view-list"
        />
        <v-text-field
          v-model="newPwd"
          label="新密码"
          type="password"
          prepend-icon="mdi-view-list"
        />
        <v-text-field
          v-model="confirmPwd"
          label="确认密码"
          type="password"
          prepend-icon="mdi-view-list"
        />
        <v-btn text color="primary" @click="modifyPwd()"> 确定 </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { toasts } from "@/utils/dialogs";
import { fApi } from "@/apis";
import { md5 } from "@/utils/md5";

export default {
  data() {
    return {
      md5,
      oldPwd: "",
      newPwd: "",
      confirmPwd: "",
    };
  },
  methods: {
    async modifyPwd() {
      if (this.newPwd != this.confirmPwd) {
        toasts.error("两次密码不一致");
        this.confirmPwd = "";
        return;
      }
      fApi.modifyPassword(md5(this.oldPwd), md5(this.newPwd))(() => {});
    },
  },
};
</script>
