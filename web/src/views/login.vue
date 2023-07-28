<template>
  <div class="pt-6">
    <v-card variant="outlined">
      <v-card-title class="headline primary white--text pt-4">
        登录&nbsp;&nbsp;
        <span style="color: #888; font-weight: bolder">
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
        <v-form v-model="isFormValid">
          <userid-input v-model="form.userId" />
          <v-text-field
            type="password"
            autocomplete="password"
            v-model="form.password"
            :rules="rules"
            label="密码"
            prepend-icon="mdi-lock"
            @keyup.native.enter="login"
            variant="outlined"
          />
          <v-btn
            color="primary"
            class="me-4 submit"
            @click="login"
            variant="outlined"
          >
            登录
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <v-card
      v-if="
        publicNotice &&
        (publicNotice.title.length > 0 || publicNotice.content.length > 0)
      "
    >
      <v-card-title v-html="publicNotice.title"></v-card-title>
      <v-card-text v-html="publicNotice.content"></v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import { fApi, fApiNotLoading, type PublicNotice } from "@/apis";
import { Categ } from "@/apis/types/enums";
import { setCurrentToken as setCurrentAxiosToken } from "@/plugins/axios";
import {
  useInfoStore,
  useLoadingStore,
  isNoRetry,
  useDialogStore,
} from "@/stores";
import { md5 } from "@/utils/md5";
import { applyNavItems } from "@/utils/nav";
import { NOT_EMPTY } from "@/utils/validation";
import { mapStores } from "pinia";
import UseridInput from "@/components/userid-input.vue";
import {
  addAssocUser,
  getDeviceUID,
  getLatestUser,
  setLatestUser,
} from "@/utils/device";
import { toasts } from "@/plugins/toastification";

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
      rules: [NOT_EMPTY()],
      isFormValid: false,
      publicNotice: null as PublicNotice,
      students: {} as Record<string, string>,
    };
  },
  beforeRouteEnter(to, from, next) {
    const infoStore = useInfoStore();
    if (infoStore.token?.length > 0 && !(infoStore.permission & Categ.None)) {
      applyNavItems();
      next("/");
    } else {
      next();
    }
  },
  beforeMount() {
    fApiNotLoading.skipOkToast.getPublicNotice()((result) => {
      this.publicNotice = result;
    });
  },
  mounted() {
    this.form.userId = getLatestUser() ?? "";
  },
  methods: {
    login() {
      if (toasts.validateForm(this.isFormValid)) {
        if (isNoRetry(this.loadingStore)) {
          toasts.error("密码错误次数过多，请稍等！");
          return;
        }
        const pwd = this.form.password;
        fApi
          .setFailedRes((res, info) => {
            if (res?.data?.noRetry) {
              this.loadingStore.noRetryStart = Date.now();
            }
          })
          .login(
            this.form.userId,
            md5(pwd),
            getDeviceUID()
          )(({ token, id }) => {
          this.infoStore.token = token;
          setCurrentAxiosToken(token);
          setLatestUser(this.form.userId);
          addAssocUser(id);
          fApi.skipOkToast.getUserInfo(id)(({ name, cls, auth, clsName }) => {
            this.infoStore.$patch({
              userId: id,
              username: name,
              permission: auth,
              classId: cls,
              className: clsName,
            });
            this.loadingStore.noRetryStart = NaN;
            applyNavItems();
            this.$router.push("/");
          });
        });
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore, useLoadingStore, useDialogStore),
  },
};
</script>
