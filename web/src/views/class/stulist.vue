<template>
  <v-card>
    <v-card-title>
      <!-- 别问我为什么520而不是500px，问就是防止用户看到完整的item就以为不能滚动 -->
      <v-menu :disabled="menudisabled" rounded max-height="520px">
        <template v-slot:activator="{ on: menu, attrs }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn depressed v-bind="attrs" v-on="{ ...tooltip, ...menu }">
                <div class="headline">{{ viewClassName }}</div>
              </v-btn>
              <div class="headline">学生列表</div>
            </template>
            <span>{{ tipText }}</span>
          </v-tooltip>
        </template>
        <v-list>
          <v-list-item v-for="(item, index) in classes" :key="index" v-on:click="changeclass(item)">
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-spacer></v-spacer>
      <v-text-field v-model="search" append-icon="mdi-magnify" label="搜索" single-line hide-details></v-text-field>
    </v-card-title>
    <v-card-text>
      <v-data-table fixed-header :headers="headers" :items="students" :search="search" @click:row="rowClick"
        loading-text="加载中..." no-data-text="没有数据哦，请选择班级" no-results-text="没有结果"></v-data-table>
      <v-dialog v-model="dialog" max-width="80%">
        <v-card>
          <stuvolist :userid="rowUserId" :title="rowUserName" />
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red darken-1" text @click="dialog = false">关闭</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { permissionTypes } from "../../utils/permissions.js";
import stuvolist from "@/components/stuvolist.vue";
import { fApi, checkToken } from "../../apis";
import { mapIsLoading, useInfoStore } from "@/stores";
import { mapStores } from "pinia";

export default {
  data: () => ({
    classes: undefined,
    students: undefined,
    search: "",
    viewClassId: "0",
    viewClassName: "UNKNOWN",
    menudisabled: true,
    dialog: false,
    rowUserId: 0,
    rowUserName: undefined,
    tipText: "班级",
    headers: [
      { text: "学号", value: "id", align: "start" },
      { text: "姓名", value: "name" },
      { text: "校内", value: "inside", sortable: false },
      { text: "校外", value: "outside", sortable: false },
      { text: "大型", value: "large", sortable: false },
      { text: "完成", value: "finished" },
    ],
  }),
  components: {
    stuvolist,
  },
  mounted () {
    this.pageload();
  },
  methods: {
    async classid2name(classid:number) {
      for (var i = 0; i < this.classes.length; i++)
        if (this.classes[i]["id"] == classid) return this.classes[i]["name"];
    },

    async pageload() {
      await checkToken();

      this.classes = await fApi.fetchClassList();

      if (this.infoStore.permission > permissionTypes.secretary) {
        this.menudisabled = false;
        this.tipText = "点击选择班级";
        if (this.$route.params.classid !== "0") {
          this.viewClassId = this.$route.params.classid;
          this.viewClassName = this.classid2name(this.viewClassId);
        } else {
          this.viewClassName = "点击选择班级";
        }
      } else {
        this.viewClassId = this.infoStore.class
        this.viewClassName = this.infoStore.classname;
      }

      if (this.viewClassId !== "0")
        await this.fetchstulist();
    },

    async fetchstulist() {
      this.students = await fApi.fetchStudentList(this.viewClassId)

      for (let i in this.students) {
        this.students[i].inside = this.timeToHint(this.students[i].inside);
        this.students[i].outside = this.timeToHint(this.students[i].outside);
        this.students[i].large = this.timeToHint(this.students[i].large);
      }
    },

    rowClick (item) {
      this.dialog = true;
      this.rowUserId = item.id;
      this.rowUserName = item.name;
    },

    changeclass (item) {
      this.viewClassId = item.id;
      this.viewClassName = item.name;
      this.fetchstulist();
    },
  },
  computed: {
    ...mapIsLoading(),
    ...mapStores(useInfoStore)
  }
};
</script>

<style>

</style>