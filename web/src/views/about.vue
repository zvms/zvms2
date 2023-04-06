<template>
  <v-container>
    <v-card>
      <v-card-title>关于ZVMS</v-card-title>
      <v-card-text>
        <p style="font-size: medium">
          <span class="f">Z</span>henhai High School
          <span class="f">V</span>olunteer <span class="f">M</span>anagement
          <span class="f">S</span>ystem
        </p>
      </v-card-text>
    </v-card>
    <v-card>
      <v-card-title>关于开发者</v-card-title>
      <v-card-text>
        <p style="font-size: larger">
          本项目初版由 neko_moyi &amp; Zecyel &amp; fpc5719 &amp; So1aric &amp;
          Solecour &amp; dblark 开发。
          <br />
          新版由 qnc &amp; _Kerman_xtr &amp; clc 开发。
          <br />
          特别感谢 7086cmd的前端初始化配置。以及zsz同学的新版图标设计。
        </p>
      </v-card-text>
    </v-card>
    <v-card>
      <v-card-title>反馈错误</v-card-title>
      <v-card-text>
        <v-form v-model="isFormValid">
          <v-textarea
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
    <v-card>
      <v-card-title>TEST</v-card-title>
      <v-card-text>
        {{ t }}
        <v-img :src="t1" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { NOTEMPTY } from "../utils/validation";
import { fApi } from "../apis";
import axios from "axios";

export default {
  name: "report",
  data() {
    return {
      report: "",
      rules: [NOTEMPTY()],
      isFormValid: false,
      t: "",
      t1: "",
    };
  },
  async mounted() {
    const keyTableApiUrl =
      "https://gitee.com/api/v5/repos/zvms/zvms-imagebed/issues/comments/17281159?access_token=bce04e8d78a6e8e5fa514aa96d79d417";

    type KeyTable = [short: string, remoteUrl: string][];
    async function fetchTable(): Promise<KeyTable> {
      const response = await axios.get(keyTableApiUrl);
      const text = response.data.body as string;
      const table = text
        .split("\n")
        .map((s) => s.split("="))
        .map((ss) => [ss[0].trim(), ss[1].trim()] as [string, string]);
      return table;
    }
    const table = await fetchTable();
    const item = table[table.length - 1];
    this.t = item[0];
    this.t1 = item[1];
  },
  methods: {
    submitReport() {
      if (this.isFormValid) {
        fApi.report(this.report)(() => {
          this.isFormValid = true;
          this.report = "";
        });
      }
    },
  },
};
</script>
<style scoped>
.f {
  font-weight: 900;
  font-size: x-large;
}
</style>
