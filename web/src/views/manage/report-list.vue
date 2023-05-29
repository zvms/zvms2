<template>
  <data-table
    fixed-header
    :headers="headers"
    :items="reports"
    @click:row="onRowClick"
  >
    <template v-slot:body v-if="reports.length === 0">
      <table-placeholder />
    </template>
  </data-table>

  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title>
        反馈信息&nbsp;&nbsp;&nbsp;from
        <v-chip
          label
          small
          @click="showStuInfo(reports[currentReport].reporter)"
        >
          {{ reports[currentReport].reporterName }}
        </v-chip>
      </v-card-title>
      <v-card-text>{{ reports[currentReport].content }}</v-card-text>
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
import { fApi, type SingleReport, type UserInfoResponse } from "@/apis";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";
import StuInfo from "@/components/stu-info.vue";
import TablePlaceholder from "@/components/table-placeholder.vue";

type DetailedSingleReport = SingleReport & {
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
          value: "time",
          key: "time",
        },
        {
          title: "内容",
          value: "shortContent",
          key: "shortContent",
        },
        {
          title: "创建者",
          value: "reporterName",
          key: "reporterName",
        },
      ],
      reports: [] as DetailedSingleReport[],
      currentReport: NaN,
      dialog: false,
      stuInfoData: undefined as any as UserInfoResponse,
      stuInfoDlg: false,
    };
  },
  beforeMount() {
    fApi.skipOkToast.fetchReport()((reports) => {
      this.reports = reports.reverse().map((v, i) => ({
        ...v,
        shortContent:
          v.content.slice(0, 20) + (v.content.length > 20 ? "..." : ""),
        index: i,
      }));
    });
  },
  methods: {
    onRowClick(ev: Event, v: any) {
      const item: DetailedSingleReport = v.item.raw;
      this.currentReport = item.index;
      this.dialog = true;
    },
    showStuInfo(id: number) {
      fApi.skipOkToast.getUserInfo(id)((info) => {
        this.stuInfoData = info;
        this.stuInfoDlg = true;
      });
    },
  },
};
</script>
