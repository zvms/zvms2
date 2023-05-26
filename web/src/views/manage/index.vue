<template>
  <v-card>
    <v-card-title> 后台管理 </v-card-title>
    <v-card-text>
      <v-tabs v-model="tab">
        <v-tab v-for="t in tabs" :value="t.id"> {{ t.name }} </v-tab>
      </v-tabs>
      <v-window v-model="tab" style="font-size: larger">
        <v-window-item v-for="t in tabs" :value="t.id">
          <component :is="t.component" />
        </v-window-item>
      </v-window>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import ModifyPwd from "./modify-pwd.vue";
import ImportTime from "./import-time.vue";
import ReportList from "./report-list.vue";
import CreateSchool from "../manage/notice-school.vue";
import CreateUser from "../manage/notice-user.vue";
import NoticeList from "./notice-list.vue";

export default {
  name: "management",
  data() {
    return {
      tab: "modify-pwd", // default tab
    };
  },
  computed: {
    tabs() {
      return [
        {
          name: "修改他人密码",
          id: "modify-pwd",
          component: ModifyPwd,
        },
        {
          name: "导入时长",
          id: "import-time",
          component: ImportTime,
        },
        {
          name: "查看反馈",
          id: "view-report",
          component: ReportList,
        },
        {
          name: "创建全校通知",
          id: "create-school",
          component: CreateSchool,
        },
        {
          name: "创建个人通知",
          id: "create-user",
          component: CreateUser,
        },
        {
          name: "查看已发通知",
          id: "report-list",
          component: NoticeList,
        },
      ];
    },
  },
};
</script>
