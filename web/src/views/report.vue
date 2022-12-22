<template>
  <v-container>
    <v-card>
      <v-card-title>反馈错误</v-card-title>
      <v-card-text>
        <v-text-field v-model="report" :rules="rules" label="问题的描述" type="text" prepend-icon="mdi-alert" />
        <v-btn text color="primary" @click="submitReport()">
          提交
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { toasts } from "../utils/dialogs";
import { NOTEMPTY } from "../utils/validation";
import { fApi } from "../apis";

export default {
  name: "report",
  data: () => ({
    report: undefined,
    rules: [NOTEMPTY()]
  }),
  mounted () {
    this.pageload();
  },
  methods: {
    pageload () {
    },
    submitReport: async function () {
      let data = await fApi.sendReport(this.report)
      if (data.type == "SUCCESS") {
        toasts.success(data.message);
      } else if (data.type == "ERROR") {
        toasts.error(data.message);
      } else {
        toasts.error("未知错误");
      }
    }
  },
};
</script>