<template>
  <v-form v-model.trim="isFormValid">
    <userid-input v-model="form.target" />
    <v-text-field
      v-model.trim="form.title"
      :rules="rules"
      type="text"
      label="通知标题"
      prepend-icon="mdi-pen"
    />
    <v-textarea
      v-model.trim="form.content"
      :rules="rules"
      type="text"
      label="通知内容"
      prepend-icon="mdi-text"
    />
    <v-text-field
      v-model.trim="form.deadtime"
      :rules="[TIME(), ...rules]"
      type="text"
      label="通知自动消失时间（e.g. 23-9-1-10-30表示23年9月1日10时30分）"
      prepend-icon="mdi-calendar-range"
    />
    <v-switch
      :label="`匿名（以“系统”名义发布）：${form.anonymous ? '是' : '否'}`"
      v-model="form.anonymous"
      prepend-icon="mdi-incognito"
    />
    <v-btn color="primary" class="submit" @click="createNotice">
      创建个人通知
    </v-btn>
  </v-form>
  <br />
</template>

<script lang="ts">
import { fApi } from "@/apis";
import { NOT_EMPTY, TIME } from "@/utils/validation";
import { confirm, validateForm } from "@/utils/dialogs";
import UseridInput from "@/components/userid-input.vue";

export default {
  name: "create-user",
  components: {
    UseridInput,
  },
  data() {
    return {
      TIME,
      form: {
        target: "",
        title: "",
        content: "",
        deadtime: "",
        anonymous: true,
      },
      rules: [NOT_EMPTY()],
      isFormValid: false,
    };
  },
  methods: {
    async createNotice() {
      if (
        validateForm(this.isFormValid) &&
        (await confirm("确定创建？一旦创建，会看见。请慎重！"))
      ) {
        let t = [parseInt(this.form.target)];
        fApi.sendUserNotice(
          t,
          this.form.title,
          this.form.content,
          this.form.deadtime
        )(() => {
          this.$router.push("/");
        });
      }
    },
  },
};
</script>
