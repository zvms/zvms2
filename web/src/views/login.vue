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
            label="学号/ID"
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
        <v-btn color="primary" block @click="login"
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
import { useNoticesStore, useInfoStore, useHeartbeatStore, useLastseenvolStore } from "@/stores";
import { md5 } from "@/utils/md5";
import { mapStores } from "pinia";
import { permissionTypes } from "@/utils/permissions";

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
              classId: cls,
              className: clsName,
              token: token,
            });
          });

          fApi.searchNotices(
            undefined,
            id
          )((result) => {
            this.noticesStore.notices = result;
          });

          this.heartbeatStore.intervalId = setInterval(() => {
            const infoStore = useInfoStore();
            if (infoStore.permission >= permissionTypes.logined) {
              console.error("!login");
              return;
            }

            this.noticesStore.notices;
            fApi.searchNotices(undefined, this.infoStore.userId);
            let flag = false;
            let last = useLastseenvolStore().lastseenvol;
            let vol = t.currentVol;

            if (
              last != null &&
              last != undefined &&
              vol != null &&
              vol != undefined
            ) {
              if (vol.length != last.length) flag = true;
              else {
                for (var i = 0; i < vol.length; i++)
                  if (vol[i]["id"] != last[i]["id"]) flag = true;
              }
            }
          }, 1000);

          applyNavItems();
          this.$router.push("/");
        });
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore, useNoticesStore, useHeartbeatStore ,useLastseenvolStore),
  },
};
</script>
