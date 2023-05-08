<template>
  <v-card>
    <v-card-title class="headline primary white--text">
      登录&nbsp;&nbsp;<span style="color: #888; font-weight: bolder">
        镇海中学义工管理系统
      </span>
      ZVMS
      <div
        style="
          font-size: x-large;
          color: #aaa;
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
      <v-form v-model.trim="isFormValid">
        <div style="height: 20px">
          {{ currentUserInfo }}
        </div>
        <userid-input v-model.trim="form.userId" />
        <v-text-field
          type="password"
          autocomplete="password"
          v-model="form.password"
          :rules="rules"
          label="密码"
          prepend-icon="mdi-lock"
          @keyup.native.enter="login"
        />
        <v-btn class="me-4 submit" @click="login">登录 </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
  <v-card
    v-if="
      publicNotice &&
      (publicNotice.title.length > 0 || publicNotice.content.length > 0)
    "
  >
    <v-card-title> 公告：{{ publicNotice.title }} </v-card-title>
    <v-card-text v-html="publicNotice.content"> </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { fApi, type PublicNotice } from "@/apis";
import { fApiNotLoading } from "@/apis/fApi";
import { Categ } from "@/apis/types/enums";
import { setCurrentToken as setCurrentAxiosToken } from "@/plugins/axios";
import router from "@/router";
import { useInfoStore, useLoadingStore } from "@/stores";
import { toasts } from "@/utils/dialogs";
import { md5 } from "@/utils/md5";
import { applyNavItems } from "@/utils/nav";
import { NOT_EMPTY } from "@/utils/validation";
import { mapStores } from "pinia";
import UseridInput from "@/components/userid-input.vue";

export default {
  name: "login",
  components: {
    UseridInput,
  },
  data() {
    return {
      form: {
        userId: "",
        password: "",
      },
      currentUserInfo: "",
      rules: [NOT_EMPTY()],
      isFormValid: false,
      publicNotice: null as PublicNotice,
      students: {} as Record<string, string>,
    };
  },
  beforeRouteEnter(to, from, next) {
    const infoStore = useInfoStore();
    if (
      infoStore.token?.length > 0 &&
      !(infoStore.permission & Categ.None)
    ) {
      next("/");
    }else{
      next()
    }
  },
  beforeMount() {
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
        fApi
          .setFailedRes((res, info) => {
            if (res?.data?.noretry) {
              this.loadingStore.noretryStart = Date.now();
            }
          })
          .login(
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
