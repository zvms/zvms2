<template>
  <v-card>
    <v-card-title
      class="headline primary white--text"
      style="backdrop-filter: blur(2px)"
      >登录</v-card-title
    >
    <br />
    <v-card-text>
      <v-form v-model="isFormValid">
        <v-text-field
          type="text"
          v-model="form.userid"
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
        <v-btn class="me-4" type="submit" @click="login">登录 </v-btn>
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
        userid: "",
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
        //this.form.password = "";
        const id = parseInt(this.form.userid);
        fApi.login(
          id,
          md5(pwd)
        )(({ token }) => {
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
            this.$router.push("/");
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
