<template>
  <data-table
    fixed-header
    :headers="headers"
    :items="notices"
    @click:row="onRowClick"
  >
    <template v-slot:body v-if="notices.length === 0">
      <table-placeholder />
    </template>
  </data-table>

  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title>
        已发通知&nbsp;&nbsp;&nbsp;from
        <v-chip label small @click="showStuInfo(notices[currentNotice].sender)">
          {{ notices[currentNotice].senderName }}
        </v-chip>
      </v-card-title>
      <v-card-text>
        {{ notices[currentNotice].content }}
      </v-card-text>
      <v-card-actions>
        <v-btn @click="deleteNotice" style="color: red"> 删除 </v-btn>
      </v-card-actions>
      <v-dialog v-model="stuInfoDlg">
        <v-card>
          <v-card-title> 用户信息 </v-card-title>
          <v-card-text>
            <StuInfo :student="stuInfoData" />
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { fApi, type SingleNotice, type UserInfoResponse } from "@/apis";
import { confirm } from "@/utils/dialogs";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";
import StuInfo from "@/components/stu-info.vue";
import TablePlaceholder from "@/components/table-placeholder.vue";

type DetailedSingleNotice = SingleNotice & {
  index: number;
  shortContent: string;
};

export default {
  name: "report-list",
  components: {
    DataTable,
    TablePlaceholder,
  },
  data() {
    return {
      headers: [
        {
          title: "发送时间",
          value: "sendtime",
          key: "sendtime",
        },
        {
          title: "标题",
          value: "title",
          key: "title",
        },
        {
          title: "内容",
          value: "shortContent",
          key: "shortContent",
        },
        {
          title: "创建者",
          value: "senderName",
          key: "senderName",
        },
      ],
      notices: [] as SingleNotice[],
      currentNotice: NaN,
      dialog: false,
      stuInfoData: undefined as any as UserInfoResponse,
      stuInfoDlg: false,
    };
  },
  beforeMount() {
    this.fetchNotices();
  },
  methods: {
    fetchNotices() {
      fApi.skipOkToast.searchNotices({})((notices) => {
        this.notices = notices.reverse().map((v, i) => ({
          ...v,
          shortContent:
            v.content.slice(0, 20) + (v.content.length > 20 ? "..." : ""),
          index: i,
        }));
      });
    },
    onRowClick(ev: Event, v: any) {
      const item: DetailedSingleNotice = v.item.raw;
      this.currentNotice = item.index;
      this.dialog = true;
    },
    showStuInfo(id: number) {
      fApi.skipOkToast.getUserInfo(id)((info) => {
        this.stuInfoData = info;
        this.stuInfoDlg = true;
      });
    },
    async deleteNotice() {
      if (await confirm("确定删除？")) {
        fApi.deleteNotice(this.notices[this.currentNotice].id)();
        this.fetchNotices();
      }
    },
  },
};
</script>
