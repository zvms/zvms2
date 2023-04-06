<template>
  <v-container>
    <v-card>
      <v-card-title>修改密码</v-card-title>
      <v-card-text>
        <v-form v-model="isFormValid">
          <v-text-field
            v-model="oldPwd"
            label="旧密码"
            type="password"
            prepend-icon="mdi-lock-outline"
            :rules="rules"
          />
          <v-text-field
            v-model="newPwd"
            label="新密码"
            type="password"
            prepend-icon="mdi-lock-outline"
            :rules="rules"
          />
          <v-text-field
            v-model="confirmPwd"
            label="确认密码"
            type="password"
            prepend-icon="mdi-lock-outline"
            :rules="rules"
          />
          <v-btn class="me-4" type="submit" color="primary" @click="modifyPwd">
            确定
          </v-btn>
          <v-btn class="me-4" @click="$router.push('/')"> 取消 </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { toasts } from "@/utils/dialogs";
import { fApi } from "@/apis";
import { md5 } from "@/utils/md5";
import { NOTEMPTY } from "@/utils/validation";

export default {
  data() {
    return {
      md5,
      oldPwd: "",
      newPwd: "",
      confirmPwd: "",
      rules: [NOTEMPTY()],
      isFormValid: false,
    };
  },
  methods: {
    modifyPwd() {
      if (this.isFormValid) {
        if (this.newPwd !== this.confirmPwd) {
          console.log("1111");
          toasts.error("两次密码不一致");
          this.confirmPwd = "";
          return;
        }
        fApi.modifyPassword(md5(this.oldPwd), md5(this.newPwd))();
      }
    },
  },
};
</script>
