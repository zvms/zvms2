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
      <permission-chips
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
    <v-card-title>
      通知
      <v-btn @click="fetchNotices" size="xsmall">
        <v-icon icon="mdi-reload" size="xsmall" />
      </v-btn>
    </v-card-title>
    <v-list shaped>
      <v-col v-if="notices.length === 0"> 没有通知哦 </v-col>
      <v-list-item
        v-else
        color="primary"
        v-for="(notice, i) in notices"
        :key="i"
        @click="showNotice(notice)"
      >
        <v-list-item-title>
          <v-icon>mdi-message</v-icon>
          {{ notice.title }}
        </v-list-item-title>
        <v-list-item-subtitle>
          来自:{{ notice.senderName }}&emsp; 发送时间:{{ notice.sendtime }}
        </v-list-item-subtitle>
        {{ notice.content }}
      </v-list-item>
    </v-list>
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
          <v-btn class="me-4 submit" @click="modifyPwd"> 确定 </v-btn>
          <v-btn class="me-4 submit" @click="pwdDialog = false"> 取消 </v-btn>
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
import router from "@/router";
import { applyNavItems } from "@/utils/nav";
import { md5 } from "@/utils/md5";
import { NOT_EMPTY } from "@/utils/validation";
import { toasts } from "@/utils/dialogs";
import { setCurrentToken as setCurrentAxiosToken } from "@/plugins/axios";
import PermissionChips from "@/components/permission-chips.vue";

export default {
  name: "me",
  components: {
    PermissionChips,
  },
  data() {
    return {
      noticeDialog: false,
      curNoticeTitle: "",
      curNoticeText: "",
      notices: [] as SingleNotice[],
      insideTime: NaN,
      outsideTime: NaN,
      largeTime: NaN,
      pwdDialog: false,
      md5,
      oldPwd: "",
      newPwd: "",
      confirmPwd: "",
      rules: [NOT_EMPTY()],
      isFormValid: false,
    };
  },
  mounted() {
    this.fetchNotices();
    if (this.timeStatVisible) {
      fApi.skipOkToast.getStudentStat(this.infoStore.userId)((stat) => {
        this.insideTime = stat.inside;
        this.outsideTime = stat.outside;
        this.largeTime = stat.large;
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
      router.push("/login");
    },
    modifyPwd() {
      if (this.isFormValid) {
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
          this.pwdDialog = false;
        });
      }
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
