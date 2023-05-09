<template>
  <v-card>
    <v-card-title>关于ZVMS</v-card-title>
    <v-card-text>
      <p style="font-size: medium">
        <span class="f">Z</span>henhai High School
        <span class="f">V</span>olunteer <span class="f">M</span>anagement
        <span class="f">S</span>ystem
        <img
          src="https://gitee.com/zvms/zvms/badge/star.svg?theme=dark"
          alt="star"
        />
      </p>
      <v-img :src="iconUrl" width="300px" class="pt-3" />
    </v-card-text>
  </v-card>
  <v-card>
    <v-card-title>关于开发者</v-card-title>
    <v-card-text>
      <p style="font-size: larger">
        本项目初版由
        <v-chip
          label
          small
          class="ma-1"
          v-for="c in contributorsV1"
          @click="showContributorInfo(c)"
        >
          {{ c.displayName }}
        </v-chip>
        开发。
        <br />
        新版由
        <v-chip
          label
          small
          class="ma-1"
          v-for="c in contributorsV2"
          @click="showContributorInfo(c)"
        >
          {{ c.displayName }}
        </v-chip>
        开发。
        <br />
        特别感谢:
        <v-chip
          label
          small
          class="ma-1"
          @click="showContributorInfo(contributorsOther._7086cmd)"
          >7086cmd</v-chip
        >的前端初始化配置, 以及<v-chip
          label
          small
          class="ma-1"
          @click="showContributorInfo(contributorsOther.zsz)"
          >zsz</v-chip
        >的新版图标设计和<v-chip
          label
          small
          class="ma-1"
          @click="showContributorInfo(contributorsOther.zjr)"
          >zjr</v-chip
        >的疯狂测试。
      </p>
    </v-card-text>
  </v-card>
  <v-card v-if="!(infoStore.permission & Categ.None)">
    <v-card-title>反馈错误</v-card-title>
    <v-card-text>
      <v-form v-model="isFormValid">
        <v-textarea
          v-model.trim="report"
          :rules="rules"
          label="问题的描述"
          type="text"
          prepend-icon="mdi-alert"
        />
        <v-btn color="primary" class="submit" @click="submitReport">
          提交
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
  <v-dialog v-model="contributorInfoDlg">
    <v-card>
      <v-card-title> 关于 {{ contributorInfo.displayName }} </v-card-title>
      <v-card-text v-html="contributorInfo.infoHtml"></v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { NOT_EMPTY } from "../utils/validation";
import { Categ, fApi } from "../apis";
import { mapStores } from "pinia";
import { useInfoStore } from "@/stores";
import { toasts } from "@/utils/dialogs";
import router from "@/router";
import {
  contributorsV1,
  contributorsV2,
  contributorsOther,
  type Contributor,
} from "@/utils/contributors";
import iconUrl from "@/assets/favicon.ico";

export default {
  name: "report",
  data() {
    return {
      Categ,
      report: "",
      rules: [NOT_EMPTY()],
      isFormValid: false,
      contributorInfoDlg: false,
      contributorInfo: undefined as any as Contributor,
      contributorsV1,
      contributorsV2,
      contributorsOther,
      iconUrl,
    };
  },
  methods: {
    submitReport() {
      if (this.isFormValid) {
        if (this.report.length > 199) {
          toasts.error("抱歉，反馈长度过长！");
          return;
        }
        fApi.report(this.report)(() => {
          router.push("/");
        });
      }
    },
    showContributorInfo(c: Contributor) {
      this.contributorInfo = c;
      this.contributorInfoDlg = true;
    },
  },
  computed: {
    ...mapStores(useInfoStore),
  },
};
</script>
<style scoped>
.f {
  font-weight: 900;
  font-size: x-large;
}
</style>
