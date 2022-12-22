<template>
  <v-card>
    <v-card-title>
      <div class="headline">班级列表</div>
      <v-spacer></v-spacer>
      <v-text-field v-model="search" append-icon="mdi-magnify" label="搜索" single-line hide-details></v-text-field>
    </v-card-title>
    <v-card-text>
      <v-table fixed-header :headers="headers" :items="classes" :search="search" @click:row="rowClick"
        loading-text="加载中..." no-data-text="没有数据哦" no-results-text="没有结果" />
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { toasts } from "../../utils/dialogs";
import { fApi, checkToken } from "../../apis";
import { permissionTypes } from "../../utils/permissions";
import { useInfoStore } from "@/stores";
import { mapStores } from "pinia";

export default {
  data() {
    return {
      classes: undefined,
      search: "",
      headers: [
        { text: "班级ID", value: "id", align: "start", sortable: true },
        { text: "班级名称", value: "name" },
      ],
    }
  },
  mounted () {
    this.pageload();
  },
  methods: {
    async pageload() {
      await checkToken();
      let classes = await fApi.fetchClassList()
      classes
        ? (this.classes = classes)
        : toasts.error("获取班级列表失败");
    },
    rowClick(item) {
      if (this.infoStore.permission >= permissionTypes.teacher)
        this.$router.push({
          name: "classStulist",
          params: { classid: item.id },
        });
      else console.log("权限不足，无法跳转");
    },
  },
  computed: {
    ...mapStores(useInfoStore)
  }
};
</script>

<style>

</style>