<template>
  <v-container>
    <v-card>
      <v-card-title>修改密码</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="pwd_old"
          label="旧密码"
          type="password"
          prepend-icon="mdi-view-list"
        />
        <v-text-field
          v-model="pwd_new"
          label="新密码"
          type="password"
          prepend-icon="mdi-view-list"
        />
        <v-text-field
          v-model="pwd_confirm"
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
      pwd_old: "",
      pwd_new: "",
      pwd_confirm: "",
    };
  },
  methods: {
    async modifyPwd() {
      if (this.pwd_new != this.pwd_confirm) {
        toasts.error("两次密码不一致");
        this.pwd_confirm = "";
        return;
      }
      fApi.modifyPassword(md5(this.pwd_old), md5(this.pwd_new))(() => {});
    },
  },
};
</script>
