<template>
  <v-container>
    <v-card>
      <v-card-title>反馈错误</v-card-title>
      <v-card-text>
        <v-form v-bind="isFormValid">
          <v-text-field
            v-model="report"
            :rules="rules"
            label="问题的描述"
            type="text"
            prepend-icon="mdi-alert"
          />
          <v-btn color="primary" type="submit" @click="submitReport">
            提交
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { NOTEMPTY } from "../utils/validation";
import { fApi } from "../apis";

export default {
  name: "report",
  data: () => ({
    report: "",
    rules: [NOTEMPTY()],
    isFormValid: false,
  }),
  methods: {
    submitReport() {
      if (this.isFormValid) {
        fApi.report(this.report)(() => {});
      }
    },
  },
};
</script>
