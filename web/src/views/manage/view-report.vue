<template>
  <data-table
    fixed-header
    :headers="headers"
    :items="reports"
    @click:row="onRowClick"
  >
    <template v-slot:body v-if="reports.length === 0">
      <p class="text-center">是空的~</p>
    </template>
  </data-table>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title>反馈信息</v-card-title>
      <v-card-text>{{ reports[currentReport].content }}</v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { fApi, type FetchReportsResponse, type SingleReport } from "@/apis";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";

type DetailedSingleReport = SingleReport & {
  index: number;
  shortContent: string;
};

export default {
  name: "view-report",
  components: {
    DataTable,
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
    };
  },
  beforeMount() {
    fApi.skipOkToast.fetchReport()((reports) => {
      this.reports = reports.reverse().map((v, i) => ({
        ...v,
        shortContent:
          v.content.slice(0, 10) + (v.content.length > 10 ? "..." : ""),
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
  },
};
</script>
