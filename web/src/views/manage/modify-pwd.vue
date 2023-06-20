<template>
  <v-form v-model="isFormValid">
    <userid-input v-model="form.userId" />
    <v-text-field
      v-model="form.newPwd"
      label="新密码 default: zvms"
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
</template>

<script lang="ts">
import { fApi } from "@/apis";
import { useInfoStore, useLoadingStore } from "@/stores";
import { toasts, confirm, validateForm } from "@/utils/dialogs";
import { md5 } from "@/utils/md5";
import { NOT_EMPTY } from "@/utils/validation";
import { mapStores } from "pinia";
import UseridInput from "@/components/userid-input.vue";

export default {
  name: "modify-pwd",
  components: {
    UseridInput,
  },
  data() {
    return {
      form: {
        userId: "",
        newPwd: "zvms",
        confirmPwd: "zvms",
      },
      rules: [NOT_EMPTY()],
      isFormValid: false,
    };
  },
  methods: {
    async modifyOthersPwd() {
      if (validateForm(this.isFormValid)) {
        if (this.form.newPwd !== this.form.confirmPwd) {
          toasts.error("两次密码不一致");
          this.form.confirmPwd = "";
          return;
        }
        if (await confirm("确定修改？")) {
          fApi.modifyOthersPassword(
            parseInt(this.form.userId),
            md5(this.form.newPwd)
          )(() => {
            this.form.userId = "";
            this.form.newPwd = "";
            this.form.confirmPwd = "";
            this.$router.push("/");
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
