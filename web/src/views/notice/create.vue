<template>
  <v-container>
    <v-card>
      <v-card-title> 创建全校通知 </v-card-title>
      <v-card-text>
        <v-form v-model="isFormValid">
          <v-text-field
            v-model="form.title"
            :rules="rules"
            type="text"
            label="通知标题"
            prepend-icon="mdi-pen"
          />
          <v-textarea
            v-model="form.content"
            :rules="rules"
            type="text"
            label="通知内容"
            prepend-icon="mdi-text"
          />
          <v-text-field
            v-model="form.deadtime"
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
            创建全校通知
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <br />
  </v-container>
</template>

<script lang="ts">
import { fApi } from "@/apis";
import { NOTEMPTY, TIME } from "@/utils/validation.js";
import { confirm } from "@/utils/dialogs";
import router from "@/router";

export default {
  data() {
    return {
      TIME,
      form: {
        title: "",
        content: "",
        deadtime: "",
        anonymous: true,
      },
      rules: [NOTEMPTY()],
      isFormValid: false,
    };
  },
  methods: {
    async createNotice() {
      if (
        this.isFormValid &&
        (await confirm("确定创建？一旦创建，全校所有人都会看见。请慎重！"))
      ) {
        fApi.sendSchoolNotice(
          this.form.anonymous,
          this.form.title,
          this.form.content,
          this.form.deadtime
        )(() => {
          router.push("/");
        });
      }
    },
  },
};
</script>
