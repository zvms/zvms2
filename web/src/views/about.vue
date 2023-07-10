<template>
  <v-card>
    <v-card-title>关于ZVMS</v-card-title>
    <v-card-text>
      <p style="font-size: medium">
        <span class="f">Z</span>
        henhai High School
        <span class="f">V</span>
        olunteer
        <span class="f">M</span>
        anagement
        <span class="f">S</span>
        ystem
      </p>
      <v-img
        src="https://img.shields.io/github/stars/zvms/zvms?logo=github"
        width="70"
        class="my-1"
        @click="toasts.info('访问github.com/zvms/zvms，给出一个star吧~')"
      ></v-img>
      <v-img
        src="https://gitee.com/zvms/zvms/badge/star.svg?theme=dark"
        width="70"
        @click="toasts.info('访问gitee.com/zvms/zvms，给出一个star吧~')"
      ></v-img>
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
          @click="showContributorInfo(contributorsOther.hhj)"
        >
          hhj
        </v-chip>
        提供和部署的校外服务器, 以及
        <v-chip
          label
          small
          class="ma-1"
          @click="showContributorInfo(contributorsOther.zsz)"
        >
          zsz
        </v-chip>
        的新版图标设计和
        <v-chip
          label
          small
          class="ma-1"
          @click="showContributorInfo(contributorsOther.zjr)"
        >
          zjr
        </v-chip>
        的疯狂测试。
      </p>
    </v-card-text>
  </v-card>
  <v-card v-if="!(infoStore.permission & Categ.None)">
    <v-card-title>反馈</v-card-title>
    <v-card-text>
      <v-form v-model="isFormValid">
        <v-textarea
          v-model.trim="report"
          :rules="rules"
          label="问题的描述"
          type="text"
          prepend-icon="mdi-comment-text-outline"
        />
        <v-btn color="primary" class="submit" @click="submitReport">提交</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
  <v-card>
    <iframe
      v-if="!(infoStore.permission & Categ.None)"
      :src="`http://${serverIP}:4001`"
      height="500px"
      width="1000px"
      seamless
      frameborder="0"
    ></iframe>
    <p v-else>登录后可以在此处查看镇中天气预报哦</p>
  </v-card>
  <v-dialog v-model="contributorInfoDlg">
    <v-card>
      <v-card-title>关于 {{ contributorInfo.displayName }}</v-card-title>
      <v-card-text v-html="contributorInfo.infoHtml"></v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { NOT_EMPTY } from "@/utils/validation";
import { Categ, fApi } from "@/apis";
import { mapStores } from "pinia";
import { useDialogStore, useInfoStore } from "@/stores";
import {
  contributorsV1,
  contributorsV2,
  contributorsOther,
  type Contributor,
} from "@/utils/contributors";
import { serverIP } from "@/plugins/axios";
import { toasts } from "@/plugins/toastification";

export default {
  name: "report",
  data() {
    return {
      Categ,
      serverIP,
      toasts,
      report: "",
      rules: [NOT_EMPTY()],
      isFormValid: false,
      contributorInfoDlg: false,
      contributorInfo: undefined as any as Contributor,
      contributorsV1,
      contributorsV2,
      contributorsOther,
    };
  },
  methods: {
    submitReport() {
      if (toasts.validateForm(this.isFormValid)) {
        if (this.report.length > 199) {
          toasts.error("抱歉，反馈长度过长！");
          return;
        }
        fApi.report(this.report)(() => {
          this.$router.push("/");
        });
      }
    },
    showContributorInfo(c: Contributor) {
      this.contributorInfo = c;
      this.contributorInfoDlg = true;
    },
  },
  computed: {
    ...mapStores(useInfoStore, useDialogStore),
  },
};
</script>
<style scoped>
.f {
  font-weight: 900;
  font-size: x-large;
}
</style>
