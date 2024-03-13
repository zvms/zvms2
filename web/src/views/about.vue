<template>
  <div>

  <VCard>
    <VCardTitle>关于ZVMS</VCardTitle>
    <VCardText>
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
      <VImg
        src="https://img.shields.io/github/stars/zvms/zvms?logo=github"
        width="70"
        class="my-1"
        @click="toasts.info('请访问 github.com/zvms/zvms，给出一个star吧~')"
      ></VImg>
      <VImg
        src="https://gitee.com/zvms/zvms/badge/star.svg?theme=dark"
        width="70"
        @click="toasts.info('请访问 gitee.com/zvms/zvms，给出一个star吧~')"
      ></VImg>
    </VCardText>
  </VCard>
  <VCard>
    <VCardTitle>关于开发者</VCardTitle>
    <VCardText>
      <p style="font-size: larger">
        本项目初版由
        <VChip
          label
          small
          class="ma-1"
          v-for="(c, idx) in contributorsV1"
          @click="showContributorInfo(c)"
          :key="idx"
        >
          {{ c.displayName }}
        </VChip>
        开发。
        <br />
        新版由
        <VChip
          label
          small
          class="ma-1"
          v-for="(c, idx) in contributorsV2"
          :key="idx"
          @click="showContributorInfo(c)"
        >
          {{ c.displayName }}
        </VChip>
        开发。
        <br />
        特别感谢:
        <VChip
          label
          small
          class="ma-1"
          @click="showContributorInfo(contributorsOther.hhj)"
        >
          hhj
        </VChip>
        提供和部署的校外服务器, 以及
        <VChip
          label
          small
          class="ma-1"
          @click="showContributorInfo(contributorsOther.zsz)"
        >
          zsz
        </VChip>
        的新版图标设计和
        <VChip
          label
          small
          class="ma-1"
          @click="showContributorInfo(contributorsOther.zjr)"
        >
          zjr
        </VChip>
        的疯狂测试。
      </p>
    </VCardText>
  </VCard>
  <VCard v-if="!(infoStore.permission & Categ.None)">
    <VCardTitle>反馈</VCardTitle>
    <VCardText>
      <VForm v-model="isFormValid">
        <VTextarea
          v-model.trim="report"
          :rules="rules"
          label="问题的描述"
          type="text"
          prepend-icon="mdi-comment-text-outline"
        />
        <VBtn color="primary" class="submit" @click="submitReport">提交</VBtn>
      </VForm>
    </VCardText>
  </VCard>
  <VCard>
    <iframe
      v-if="!(infoStore.permission & Categ.None)"
      :src="`http://${serverIP}:4001`"
      height="500px"
      width="1000px"
      seamless
      frameborder="0"
    ></iframe>
    <p v-else>登录后可以在此查看镇中天气预报</p>
  </VCard>
  <VDialog v-model="contributorInfoDlg">
    <VCard>
      <VCardTitle>关于 {{ contributorInfo.displayName }}</VCardTitle>
      <VCardText v-html="contributorInfo.infoHtml"></VCardText>
    </VCard>
  </VDialog>
  </div>
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
