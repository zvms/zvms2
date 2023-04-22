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
          autocomplete="userid"
          v-model="form.userId"
          :rules="rules"
          label="学号/ID"
        />
        <v-text-field
          type="password"
          autocomplete="password"
          v-model="form.password"
          :rules="rules"
          label="密码"
          @keyup.native.enter="login"
        />
        <v-btn class="me-4 submit" @click="login">登录 </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
  <v-card v-if="publicNotice">
    <v-card-title> 公告：{{ publicNotice.title }} </v-card-title>
    <v-card-text v-html="publicNotice.content"> </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { fApi, type PublicNotice } from "@/apis";
import { ForegroundApi } from "@/apis/fApi";
import { Categ } from "@/apis/types/enums";
import { setCurrentToken as setCurrentAxiosToken } from "@/plugins/axios";
import router from "@/router";
import { useInfoStore, useLoadingStore } from "@/stores";
import { toasts } from "@/utils/dialogs";
import { md5 } from "@/utils/md5";
import { applyNavItems } from "@/utils/nav";
import { NOT_EMPTY } from "@/utils/validation";
import { mapStores } from "pinia";

export default {
  name: "login",
  data() {
    return {
      form: {
        userId: "",
        password: "",
      },
      rules: [NOT_EMPTY()],
      isFormValid: false,
      publicNotice: null as PublicNotice,
    };
  },
  mounted() {
    if (this.infoStore.token && !(this.infoStore.permission & Categ.None)) {
      router.push("/");
    }
    fApi.skipOkToast.getPublicNotice()((result) => {
      this.publicNotice = result;
    });
  },
  methods: {
    login() {
      if (this.isFormValid) {
        if (this.loadingStore.noretry) {
          toasts.error("密码错误次数过多，请稍等！");
          return;
        }
        const pwd = this.form.password;
        const sepcialFApi = new ForegroundApi({
          beforeReq(info) {},
          errorReq(e: Error, info) {},
          successedRes(res, info) {},
          failedRes: (res, info) => {
            if (res?.data?.noretry) {
              this.loadingStore.noretryStart = Date.now();
            }
          },
          afterProcess(info) {},
          errorProcess(e, info) {},
          cleanup(info) {},
          defaultFailedToast: true,
          defaultOkToast: true,
        });
        sepcialFApi.login(
          this.form.userId,
          md5(pwd)
        )(({ token, id }) => {
          this.infoStore.token = token;
          setCurrentAxiosToken(token);
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
    ...mapStores(useInfoStore, useLoadingStore),
  },
};
</script>
