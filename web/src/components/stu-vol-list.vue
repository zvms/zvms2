<template>
  <v-card flat>
    <v-card-title>
      <div class="headline">{{ title }} 义工列表</div>
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="搜索"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-card-text>
      <v-data-table
        fixed-header
        :headers="headers"
        :items="volworks"
        :search="search"
        @click:row="rowClick"
        loading-text="加载中..."
        no-data-text="没有数据哦"
        no-results-text="没有结果"
      >
      </v-data-table>
    </v-card-text>
    <v-dialog v-model="dialog" max-width="80%">
      <v-card>
        <volcert :volid="volid" :stuid="stuid" :stuname="stuname" />
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="dialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script lang="ts">
import { fApi } from "../apis";
import volcert from "./vol-cert.vue";

export default {
  name: "stu-vol-list",
  props: ["userid", "title"],
  components: {
    volcert,
  },
  data: () => ({
    stuid: NaN,
    volid: NaN,
    dialog: false,
    search: "",
    headers: undefined as any,
  }),
  methods: {
    async updateVol() {
      if (Number.isFinite(this.userid) && Number.isFinite(this.userid)) {
        fApi.searchVolunteers(
          undefined,
          this.userid
        )((result) => {
          this.headers = [
            { text: "义工ID", value: "volId", align: "start", sortable: true },
            { text: "义工名称", value: "name" },
            { text: "大型时长（单位：分钟）", value: "reward" },
            { text: "完成状态", value: "status" },
          ];
        });
      }
    },
    rowClick(item) {
      this.volid = item.volId;
      this.stuid = this.userid;
      this.stuname = this.title;
      this.dialog = true;
    },
  },
  watch: {
    userid: {
      immediate: true,
      handler() {
        this.updateVol();
      },
    },
  },
};
</script>
