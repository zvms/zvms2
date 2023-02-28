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
        <vol-info :vol="currentVol" />
        <thought-info :thought="currentThought" />
        <v-spacer />
        发放的{{ getVolTypeName(vol.type) }}时长（分钟）
        <v-text-field
          v-model="currentReward"
          label="不填为默认值"
          prepend-icon="mdi-view-list"
        />
        <v-card-actions>
          <v-spacer />
          <v-btn color="green" @click="audit(true)">通过 </v-btn>
          <v-btn color="yellow" @click="audit(false)">打回 </v-btn>
          <!-- <v-btn color="primary" @click="dialog1 = false">取消 </v-btn> -->
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
import {
  VolStatus,
  fApi,
  getVolTypeName,
  type Thought,
  type VolunteerInfoResponse,
  type ThoughtInfoResponse,
  ThoughtStatus,
} from "@/apis";
import { mapIsLoading, useInfoStore } from "@/stores";
import { timeToHint } from "@/utils/calc";
import { mapStores } from "pinia";
import { VDataTable } from "vuetify/labs/VDataTable";
import ThoughtInfo from "@/components/thought-info.vue";
import VolInfo from "@/components/vol-info.vue";

export default {
  components: {
    VDataTable,
    VolInfo,
    ThoughtInfo,
  },
  data() {
    return {
      timeToHint,
      getVolTypeName,

      headers: [
        { title: "义工编号", value: "volId", align: "start", sortable: true },
        { title: "学号", value: "stuId" },
      ],

      thoughts: [] as Thought[],

      dialog1: false,
      currentVol: undefined as VolunteerInfoResponse | undefined,
      currentThought: undefined as ThoughtInfoResponse | undefined,
      currentReward: NaN,
    };
  },
  mounted() {
    fApi.searchThoughts(
      undefined,
      ThoughtStatus.WaitingForFinalAudit
    )((result) => {
      this.thoughts = result;
    });
  },
  methods: {
    rowClick(
      event: Event,
      value: {
        item: DataTableItem;
      }
    ) {
      fApi.getThoughtInfo(
        item.volid,
        item.stuid
      )((thought) => {
        this.currentVol = vol;
        this.currentThought = thought;
        this.dialog1 = true;
      });
    },
    /**
     * @param status `true` for ok.
     */
    async audit(status: boolean) {
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
          [this.currentReward],
          [validateNotNAN(), validateNotNegative(), validateNotLargerThan(4)]
        );

        fApi.finalAudit(
          this.currentThought.volId,
          this.curre
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
