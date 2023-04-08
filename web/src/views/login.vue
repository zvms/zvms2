<template>
  <v-card>
    <v-card-title class="headline primary white--text">
      登录&nbsp;&nbsp;<span style="color: #888; font-weight: bolder"
        >镇海中学义工管理系统</span
      >
      ZVMS
      <div
        style="
          font-size: x-large;
          color: gray;
          text-align: right;
          margin-bottom: -6px;
          padding-top: 14px;
          margin-top: -34px;
        "
      >
        励志&nbsp;&nbsp;进取&nbsp;&nbsp;勤奋&nbsp;&nbsp;健美
      </div>
    </v-card-title>
    <v-card-text>
      <v-form v-model="isFormValid">
        <v-text-field
          type="text"
          v-model="form.userId"
          :rules="rules"
          label="学号/ID"
        />
        <v-text-field
          type="password"
          v-model="form.password"
          :rules="rules"
          label="密码"
          @keyup.native.enter="login"
        />
        <v-btn class="me-4 submit" @click="login">登录 </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { fApi } from "../apis";
import { NOTEMPTY } from "../utils/validation.js"; //校验表单完整性
import { applyNavItems } from "../utils/nav";
import { useInfoStore, useHeartbeatStore } from "@/stores";
import { md5 } from "@/utils/md5";
import { mapStores } from "pinia";
import { Categ } from "@/apis/types/enums";
import router from "@/router";

export default {
  name: "login",
  data() {
    return {
      form: {
        userId: "",
        password: "",
      },
      rules: [NOTEMPTY()],
      isFormValid: false,
    };
  },
  mounted() {
    if (this.infoStore.token && !(this.infoStore.permission & Categ.None)) {
      router.push("/");
    }
  },
  methods: {
    login() {
      if (this.isFormValid) {
        const pwd = this.form.password;
        fApi.login(
          this.form.userId,
          md5(pwd)
        )(({ token, id }) => {
          this.infoStore.token = token;
          fApi.skipOkToast.getUserInfo(id)(({ name, cls, auth, clsName }) => {
            this.infoStore.$patch({
              userId: id,
              username: name,
              permission: auth,
              classId: cls,
              className: clsName,
            });

            applyNavItems();
            router.push("/");
          });
        });
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore, useHeartbeatStore),
  },
};
</script>
