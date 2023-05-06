<template>
  <v-card>
    <v-card-title>修改他人密码</v-card-title>
    <v-card-text>
      <v-form v-model="isFormValid">
        <userid-input
          v-model.trim="form.userId"
        />
        <v-text-field
          v-model="form.newPwd"
          label="新密码"
          type="password"
          prepend-icon="mdi-lock-outline"
          :rules="rules"
        />
        <v-text-field
          v-model="form.confirmPwd"
          label="确认密码"
          type="password"
          prepend-icon="mdi-lock-outline"
          :rules="rules"
          @keyup.native.enter="modifyOthersPwd"
        />
        <v-btn class="me-4 submit" @click="modifyOthersPwd">修改密码</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { fApi } from "@/apis";
import { useInfoStore, useLoadingStore } from "@/stores";
import { toasts, confirm } from "@/utils/dialogs";
import { md5 } from "@/utils/md5";
import { NOT_EMPTY } from "@/utils/validation";
import { mapStores } from "pinia";
import UseridInput from "@/components/userid-input.vue";

export default {
  name: "management",
  components:{
    UseridInput,
  },
  data() {
    return {
      form: {
        userId: "",
        newPwd: "",
        confirmPwd: "",
      },
      rules: [NOT_EMPTY()],
      isFormValid: false,
    };
  },
  methods: {
    async modifyOthersPwd() {
      if (this.isFormValid) {
        if (this.form.newPwd !== this.form.confirmPwd) {
          toasts.error("两次密码不一致");
          this.form.confirmPwd = "";
          return;
        }
        if (await confirm("确定修改？")) {
          fApi
            .modifyotherspassword(
              parseInt(this.form.userId),
              md5(this.form.newPwd)
            )(() => {
            this.form.userId = "";
            this.form.newPwd = "";
            this.form.confirmPwd = "";
          });
        }
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore, useLoadingStore),
  },
};
</script>
