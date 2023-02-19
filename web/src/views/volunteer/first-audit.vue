<template>
  <v-container>
    <v-card>
      <v-card-title>
        未审核感想列表
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
          :items="thoughts"
          :search="search"
          @click:row="rowClick"
          loading-text="加载中..."
          no-data-text="没有数据哦"
          no-results-text="没有结果"
        >
        </v-data-table>
      </v-card-text>
    </v-card>
    <v-dialog v-model="dialog1" max-width="80%">
      <v-card>
        <v-card-title>详细信息</v-card-title>
        <v-simple-table style="margin: 20px">
          <tbody>
            <tr>
              <td>义工编号</td>
              <td>{{ volid }}</td>
            </tr>
            <tr>
              <td>义工日期</td>
              <td>{{ volDate }}</td>
            </tr>
            <tr>
              <td>义工时间</td>
              <td>{{ volTime }}</td>
            </tr>
            <tr>
              <td>义工详细信息</td>
              <td>{{ volDesc }}</td>
            </tr>
            <tr>
              <td>{{ getVolTypeName(currentThought!.type) }}时长</td>
              <td>{{ timeToHint(reward) }}</td>
            </tr>
            <tr>
              <td>参与者</td>
              <td>{{ stuid }} {{ stuname }}</td>
            </tr>
            <tr>
              <td>感想</td>
              <td>{{ thought }}</td>
            </tr>
            <tr v-if="pictures">
              <td>图片</td>
              <td>
                <ul v-for="img in pictures" :key="img.id">
                  <li>
                    <img
                      :src="'data:image/png;base64,' + img.src"
                      class="pic"
                    />
                  </li>
                </ul>
              </td>
            </tr>
            <tr>
              <td>发放的{{ getVolTypeName(vol.type) }}时长（分钟）</td>
              <td>
                <v-text-field
                  v-model="reward"
                  label="不填为默认值"
                  prepend-icon="mdi-view-list"
                />
              </td>
            </tr>
          </tbody>
        </v-simple-table>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="audit(1)">通过 </v-btn>
          <v-btn color="red" @click="audit(2)">拒绝 </v-btn>
          <v-btn color="yellow" @click="audit(3)">打回 </v-btn>
          <v-btn color="primary" @click="dialog1 = false">取消 </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { confirm } from "@/utils/dialogs";
import {
  validate,
  validateNotNAN,
  validateNotLargerThan,
  validateNotNegative,
} from "@/utils/validation";
import { VolStatus, fApi, getVolTypeName, type SingleVolunteer, ThoughtStatus, type SearchThoughts, type Thought } from "@/apis";
import { mapIsLoading, useInfoStore } from "@/stores";
import { timeToHint } from "@/utils/calc";
import { mapStores } from "pinia";

export default {
  data() {
    return {
      timeToHint,
      getVolTypeName,
      search: "",
      headers: [
        { text: "义工编号", value: "volId", align: "start", sortable: true },
        { text: "学号", value: "stuId" },
      ],
      singleVols: [] as Thought[],
      dialog1: false,
      stuid: NaN,
      volid: NaN,
      thought: "",
      currentThought: undefined as Thought | undefined,
      reward: NaN,

      pictures: [],
    };
  },
  mounted() {
    // const permisson = this.infoStore.permission;
    // this.auditType =( permission & (permissionTypes.teacher|permissionTypes.admin|permissionTypes._super|permissionTypes.system))?
    //   "final":(permission&permissionTypes.secretary)?"first"|"error";
    fApi.searchThoughts(
      this.infoStore.classId,
      ThoughtStatus.WaitingForFirstAudit
    )((result:Thought[]) => {
      this.singleVols = result;
    });
  },
  methods: {
    rowClick(item) {
      this.dialog1 = true;
      this.volid = item.volId;
      this.stuid = item.stuId;
      this.thought = item.thought;
      this.pictures = item.picture;

      fApi.getSingleThoughtInfo(
        this.volid,
        this.stuid
      )((result) => {
        this.currentThought = result;
      });

      this.volDate = vol.date;
      this.volTime = vol.time;
      this.volDesc = vol.description;
      this.volTI = vol.inside;
      this.volTO = vol.outside;
      this.volTL = vol.large;
    },
    async audit(status) {
      let value = await confirm();
      if (value) {
        this.dialog1 = false;
        if (status == 1) {
          if (this.inside == undefined || this.inside == "")
            this.inside = this.volTI;
          if (this.outside == undefined || this.outside == "")
            this.outside = this.volTO;
          if (this.large == undefined || this.large == "")
            this.large = this.volTL;
        } else {
          this.inside = "0";
          this.outside = "0";
          this.large = "0";
        }

        validate(
          [this.inside, this.outside, this.large],
          [validateNotNAN(), validateNotNegative(), validateNotLargerThan(4)]
        );

        fApi.firstAudit(
          this.stuid,
          status
        )((result) => {
          this.volDate = data.date;
          this.volTime = data.time;
          this.volDesc = data.description;
          this.volTI = data.inside;
          this.volTO = data.outside;
          this.volTL = data.large;
        });
        this.inside = undefined;
        this.outside = undefined;
        this.large = undefined;
        this.pageload();
      }
    },
  },
  computed: {
    ...mapIsLoading(),
    ...mapStores(useInfoStore),
  },
};
</script>

<style scoped>
.v-card {
  margin: 0.3rem;
}

.pic {
  width: auto;
  height: 120px;
}
</style>
