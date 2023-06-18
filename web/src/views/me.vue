<template>
  <v-card>
    <v-card-title>
      你好,
      <strong>{{ infoStore.username }}</strong>
      <span
        style="
          font-size: x-large;
          color: #aaa;
          text-align: right;
          float: right;
          transform: translateY(5px);
        "
      >
        励志&nbsp;&nbsp;进取&nbsp;&nbsp;勤奋&nbsp;&nbsp;健美
      </span>
    </v-card-title>
    <v-card-text>
      <user-chips
        :permission="infoStore.permission"
        :className="infoStore.className"
      />
    </v-card-text>
    <v-card-actions>
      <v-btn @click="pwdDialog = true">修改密码</v-btn>
      <v-btn @click="logout">登出</v-btn>
    </v-card-actions>
  </v-card>
  <v-card v-if="timeStatVisible">
    <v-card-title>您在系统上的义工时间</v-card-title>
    <v-card-text style="font-size: medium">
      校内义工：{{ insideTime }}
      <br />
      校外义工：{{ outsideTime }}
      <br />
      大型义工：{{ largeTime }}
      <p style="font-size: small">注：不包括纸质义工本上的时间哦。</p>
    </v-card-text>
  </v-card>
  <v-card>
    <v-card-title>
      通知
      <v-btn @click="fetchNotices" size="xsmall">
        <v-icon icon="mdi-reload" size="xsmall" />
      </v-btn>
    </v-card-title>
    <p v-if="notices.length === 0">没有通知哦</p>
    <infinite-scroll
      v-else
      :items="displayedNotices"
      @load="loadNotice"
      empty-text="没有更多通知了..."
      style="margin-top: -22px"
    >
      <template v-for="notice in displayedNotices" :key="notice.sendtime">
        <v-list-item @click="showNotice(notice)">
          <v-list-item-title>
            <v-icon>mdi-message-text</v-icon>
            {{ notice.title }}
          </v-list-item-title>
          <v-list-item-subtitle>
            来自:{{ notice.senderName }}&emsp; 发送时间:{{ notice.sendtime }}
          </v-list-item-subtitle>
          {{ notice.content }}
        </v-list-item>
      </template>
      <template v-slot:load-more="{ props }">
        <v-btn style="border: 1px grey solid" v-bind="props">
          加载更多通知
        </v-btn>
      </template>
    </infinite-scroll>
  </v-card>

  <v-dialog v-model="noticeDialog">
    <v-card>
      <v-card-title>{{ curNoticeTitle }}</v-card-title>
      <v-card-text>
        <pre>{{ curNoticeText }}</pre>
      </v-card-text>
    </v-card>
  </v-dialog>

  <v-dialog v-model="pwdDialog">
    <v-card>
      <v-card-title>修改密码</v-card-title>
      <v-card-text>
        <v-form v-model="isFormValid">
          <v-text-field
            v-model="oldPwd"
            label="旧密码"
            type="password"
            prepend-icon="mdi-lock-outline"
            :rules="rules"
          />
          <v-text-field
            v-model="newPwd"
            label="新密码"
            type="password"
            prepend-icon="mdi-lock-outline"
            :rules="rules"
          />
          <v-text-field
            v-model="confirmPwd"
            label="确认密码"
            type="password"
            prepend-icon="mdi-lock-outline"
            :rules="rules"
          />
          <v-btn class="me-4 submit" @click="modifyPwd">确定</v-btn>
          <v-btn class="me-4 submit" @click="pwdDialog = false">取消</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { useInfoStore } from "@/stores";
import { fApi, type SingleNotice, type NoticeBody } from "@/apis";
import { Categ } from "@/apis/types/enums";
import { mapStores } from "pinia";
import { applyNavItems } from "@/utils/nav";
import { timeToHint } from "@/utils/calc";
import { md5 } from "@/utils/md5";
import { NOT_EMPTY } from "@/utils/validation";
import { toasts, validateForm } from "@/utils/dialogs";
import { setCurrentToken as setCurrentAxiosToken } from "@/plugins/axios";
import PermissionChips from "@/components/user-chips.vue";
import { VInfiniteScroll as InfiniteScroll } from "vuetify/labs/VInfiniteScroll";

export default {
  name: "me",
  components: {
    PermissionChips,
    InfiniteScroll,
  },
  data() {
    return {
      noticeDialog: false,
      curNoticeTitle: "",
      curNoticeText: "",
      notices: [] as SingleNotice[],
      displayedNotices: [] as SingleNotice[],
      insideTime: "加载中...",
      outsideTime: "加载中...",
      largeTime: "加载中...",
      pwdDialog: false,
      md5,
      oldPwd: "",
      newPwd: "",
      confirmPwd: "",
      rules: [NOT_EMPTY()],
      isFormValid: false,
    };
  },
  beforeMount() {
    this.fetchNotices();
    if (this.timeStatVisible) {
      fApi.skipOkToast.getStudentStat(this.infoStore.userId)((stat) => {
        this.insideTime = timeToHint(stat.inside);
        this.outsideTime = timeToHint(stat.outside);
        this.largeTime = timeToHint(stat.large);
      });
    }
  },
  methods: {
    fetchNotices() {
      fApi.skipOkToast.searchNotices({
        school: 1,
      })((result1) => {
        fApi.skipOkToast.searchNotices({
          receiver: this.infoStore.userId,
        })((result2) => {
          this.notices = [...result1.reverse(), ...result2.reverse()];
          this.displayedNotices = this.notices.slice(0, 3);
        });
      });
    },
    showNotice(notice: NoticeBody) {
      this.curNoticeTitle = notice.title;
      this.curNoticeText = notice.content;
      this.noticeDialog = true;
    },
    logout() {
      fApi.logout()(() => {
        setCurrentAxiosToken("");
      });
      useInfoStore().$reset();
      applyNavItems();
      this.$router.push("/login");
    },
    modifyPwd() {
      if (validateForm(this.isFormValid)) {
        if (this.newPwd !== this.confirmPwd) {
          toasts.error("两次密码不一致");
          this.confirmPwd = "";
          return;
        }
        fApi.modifyPassword(
          md5(this.oldPwd),
          md5(this.newPwd)
        )(() => {
          this.oldPwd = "";
          this.newPwd = "";
          this.confirmPwd = "";
          this.pwdDialog = false;
        });
      }
    },
    async loadNotice({ done }: any) {
      const len = this.displayedNotices.length;
      if (len === this.notices.length) {
        done("empty");
        return;
      }
      this.displayedNotices.push(...this.notices.slice(len, len + 3));
      if (len + 3 >= this.notices.length) {
        done("empty");
        return;
      }
      done("ok");
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    timeStatVisible() {
      return this.infoStore.permission & Categ.Student;
    },
  },
};
</script>
