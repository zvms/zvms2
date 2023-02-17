<template>
  <v-card
    id="bgcard"
    class="d-flex mb-6 align-center justify-center"
    outlined
    color="rgba(255, 255, 255, 0)"
  >
    <v-card class="mx-auto" width="50%" max-width="500" min-width="250">
      <v-card-title
        class="headline primary white--text"
        style="backdrop-filter: blur(2px)"
        >登录</v-card-title
      >
      <br />
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            type="username"
            v-model="form.userid"
            :rules="rules"
            label="用户ID"
            @keyup.native.enter="login"
          />
          <v-text-field
            type="password"
            v-model="form.password"
            :rules="rules"
            label="密码"
            @keyup.native.enter="login"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" block :disabled="isLoading" @click="login"
          >登录</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-card>
</template>

<script lang="ts">
import { fApi } from "../apis";
import { NOTEMPTY } from "../utils/validation.js"; //校验表单完整性
import { applyNavItems } from "../utils/nav";
import { useNoticesStore, useInfoStore } from "@/stores";
import { md5 } from "@/utils/md5";
import { mapStores } from "pinia";

export default {
  name: "login",
  data() {
    return {
      form: {
        userid: "",
        password: "",
      },
      rules: [NOTEMPTY()],
    } satisfies {
      form: {
        userid: string;
        password: string;
      };
      rules: any[];
    };
  },
  methods: {
    login() {
      if (this.$refs.form.validate()) {
        this.form.password = "";
        const id = parseInt(this.form.userid);
        fApi.login(
          id,
          md5(this.form.password)
        )(({ token }) => {
          fApi.getUserInfo(id)(({ name, cls, auth, clsName }) => {
            this.infoStore.$patch({
              username: name,
              permission: auth,
              class: cls,
              classname: clsName,
              token: token,
            });
          });
          fApi.searchNotices(
            undefined,
            id
          )((result) => {
            this.noticesStore.notices = result;
          });
          applyNavItems();
          this.$router.push("/me");
        });
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore, useNoticesStore),
  },
};
</script>
