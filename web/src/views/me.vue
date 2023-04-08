<template>
  <v-card>
    <v-card-title>
      你好,
      <strong>{{ infoStore.username }}</strong>
      <span
        style="
          font-size: x-large;
          color: #999;
          text-align: right;
          float: right;
          transform: translateY(5px);
        "
      >
        励志&nbsp;&nbsp;进取&nbsp;&nbsp;勤奋&nbsp;&nbsp;健美
      </span>
    </v-card-title>
    <v-card-text>
      <v-chip v-for="chip in chips" :key="chip.id" class="ma-2">
        <v-icon left>{{ chip.icon }}</v-icon>
        {{ chip.content }}
      </v-chip>
    </v-card-text>
    <v-card-actions>
      <v-btn @click="modifyPwd">修改密码</v-btn>
      <v-btn @click="logout">登出</v-btn>
    </v-card-actions>
  </v-card>
  <v-card v-if="timeStatVisible">
    <v-card-title> 您在系统上的义工时间 </v-card-title>
    <v-card-text style="font-size: medium">
      校内义工：{{ insideTime }} 分钟
      <br />
      校外义工：{{ outsideTime }} 分钟
      <br />
      大型义工：{{ largeTime }} 分钟
      <p style="font-size: small">注：不包括纸质义工本上的时间哦。</p>
    </v-card-text>
  </v-card>
  <v-card>
    <v-card-title> 通知 </v-card-title>
    <v-list shaped>
      <v-col v-if="notices.length === 0"> 没有通知哦 </v-col>
      <v-list-item
        v-else
        color="primary"
        v-for="(notice, i) in notices"
        :key="i"
        @click="showNotice(notice)"
      >
        <v-list-item icon>
          <v-icon>mdi-message</v-icon>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>{{ notice.title }}</v-list-item-title>
          <v-list-item-subtitle>{{ notice.content }}</v-list-item-subtitle>
        </v-list-item>
      </v-list-item>
    </v-list>
  </v-card>

  <v-dialog v-model="noticeDialog" max-width="80%">
    <v-card>
      <v-card-title>{{ curNoticeTitle }}</v-card-title>
      <v-card-text v-html="curNoticeText"></v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { useInfoStore } from "@/stores";
import { fApi, type SingleNotice, type NoticeBody } from "@/apis";
import { Categ, getCategName } from "@/apis/types/enums";
import { mapStores } from "pinia";
import router from "@/router";
import { applyNavItems } from "@/utils/nav";

export default {
  name: "me",
  data() {
    return {
      noticeDialog: false,
      curNoticeTitle: "",
      curNoticeText: "",
      notices: [] as SingleNotice[],
      insideTime: NaN,
      outsideTime: NaN,
      largeTime: NaN,
    };
  },
  mounted() {
    fApi.skipOkToast.searchNotices({
      user: this.infoStore.userId,
    })((result) => {
      this.notices = result;
    });
    if (this.timeStatVisible) {
      fApi.skipOkToast.getStudentStat(this.infoStore.userId)((stat) => {
        this.insideTime = stat.inside;
        this.outsideTime = stat.outside;
        this.largeTime = stat.large;
      });
    }
  },
  methods: {
    showNotice(notice: NoticeBody) {
      this.curNoticeTitle = notice.title;
      let s = "";
      for (const c of notice.content) {
        if (c == "\n") {
          s += "<br />";
        } else {
          s += c;
        }
      }
      this.curNoticeText = s;
      this.noticeDialog = true;
    },
    logout() {
      fApi.logout()(() => {
        useInfoStore().$reset();
        applyNavItems();
        router.push("/login");
      });
    },
    modifyPwd() {
      router.push("/modifyPwd");
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    chips(): { id: number; icon: string; content: string }[] {
      return [
        {
          id: 0,
          icon: "mdi-account-multiple",
          content: this.infoStore.className,
        },
        ...[2, 4, 8, 16, 32, 64]
          .filter((id) => id & this.infoStore.permission)
          .map((id) => ({
            id,
            icon: "mdi-check-decagram",
            content: getCategName(id),
          })),
      ];
    },
    timeStatVisible() {
      return this.infoStore.permission & Categ.Student;
    },
  },
};
</script>
