<template>
  <v-container>
    <v-card>
      <v-card-title>修改密码</v-card-title>
      <v-card-text>
        <v-text-field v-model="pwd_old" label="旧密码" type="password" prepend-icon="mdi-view-list" />
        <v-text-field v-model="pwd_new" label="新密码" type="password" prepend-icon="mdi-view-list" />
        <v-text-field v-model="pwd_conf" label="确认密码" type="password" prepend-icon="mdi-view-list" />
        <v-btn text color="primary" @click="modifyPwd()">
          确定
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { toasts } from "../utils/dialogs";
import { checkToken, fApi } from "../apis"

var md5 = require('md5-node');
export default {
  data: () => ({
    pwd_old: undefined,
    pwd_new: undefined,
    pwd_conf: undefined
  }),
  mounted () {
    this.pageload();
  },
  methods: {
    pageload: async function () {
      await checkToken();
    },
    modifyPwd: async function () {
      if (this.pwd_new != this.pwd_conf) {
        toasts.error("两次密码不一致");
        return;
      }

      let data = await fApi.modifyPwd(md5(this.pwd_old), md5(this.pwd_new))
      if (data.type == "SUCCESS") {
        toasts.success(data.message);
      } else {
        toasts.error(data.message);
      }
    }
  },
};
</script>
