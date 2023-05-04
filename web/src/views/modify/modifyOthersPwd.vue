<template>
    <v-card>
      <v-card-title>修改他人密码</v-card-title>
      <v-card-text>
        <v-form v-model.trim="isFormValid">
          <div style="height:20px">
          {{ currentUserInfo }}
          </div>
          <v-text-field
            type="text"
            autocomplete="userid"
            v-model.trim="form.userId"
            :rules="rules"
            label="ID/学号 &nbsp;&nbsp; e.g. 20221145"
            @update:model-value="updateCurrentUserInfo"
          />
          <v-text-field
            type="password"
            autocomplete="password"
            v-model="form.password"
            :rules="rules"
            label="密码"
            @keyup.native.enter="modifyOthersPwd"
          />
          <v-btn class="me-4 submit" @click="modifyOthersPwd">修改密码</v-btn>
        </v-form>
      </v-card-text>
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

export default {
  name: "login",
  data() {
    return {
      form: {
        userId: "",
        password: "",
      },
      currentUserInfo: "",
      rules: [NOT_EMPTY()],
      isFormValid: false,
      //publicNotice: null as PublicNotice,
      students: {} as Record<string, string>,
    };
  },
  
  // beforeMount() {
  //   if (this.infoStore.token && !(this.infoStore.permission & Categ.None)) {
  //     router.push("/");
  //   }
  //   fApi.skipOkToast.getPublicNotice()((result) => {
  //     this.publicNotice = result;
  //   });
  //   //
  //   // (async () => {
  //   //   this.students = ;
  //   // })();
  // },
  
  methods: {
    updateCurrentUserInfo() {
      const userId = parseInt(this.form.userId);
      if (!Number.isFinite(userId) || ("" + userId).length !== 8) {
        this.currentUserInfo = "";
        return;
      }
      fApiNotLoading.skipOkToast.getUserBasicInfo(userId)(({clsName,userName}) => {
        this.currentUserInfo = `${clsName} ${userName}`;
      });
    },
    modifyOthersPwd() {
      if (this.isFormValid) {
        // if (this.loadingStore.noretry) {
        //   toasts.error("密码错误次数过多，请稍等！");
        //   return;
        // }
        const pwd = this.form.password;
        fApi
          .setFailedRes((res, info) => {
            if (res?.data?.noretry) {
              this.loadingStore.noretryStart = Date.now();
            }
          })
          .modifyotherspassword(
            parseInt(this.form.userId),
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
