<template>
  <v-container>
    <v-card>
      <v-card-title> 未审核感想列表 </v-card-title>
      <v-card-text>
        <data-table
          fixed-header
          :headers="headers"
          :items="thoughts"
          @click:row="rowClick"
          loading-text="加载中..."
          no-data-text="没有数据哦"
          no-results-text="没有结果"
        >
        </data-table>
      </v-card-text>
    </v-card>
    <v-dialog v-model="dialog1" max-width="80%">
      <v-card>
        <v-card-title>详细信息</v-card-title>
        <vol-info v-if="currentVol" :vol="currentVol" />
        <thought-info v-if="currentThought" :thought="currentThought" />
        <v-spacer />
        发放的{{ getVolTypeName(currentVol!.type) }}时长（分钟）
        <v-text-field
          v-model="currentReward"
          label="不填为默认值"
          prepend-icon="mdi-view-list"
        />
        <v-card-actions>
          <v-spacer />
          <v-btn color="green" @click="audit(true)">通过 </v-btn>
          <v-btn color="red" @click="audit(false)">打回 </v-btn>
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
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";
import ThoughtInfo from "@/components/thought-info.vue";
import VolInfo from "@/components/vol-info.vue";

export default {
  components: {
    DataTable,
    VolInfo,
    ThoughtInfo,
  },
  data() {
    return {
      timeToHint,
      getVolTypeName,

      headers: [
        {
          key: "volId",
          title: "义工编号",
          value: "volId",
          align: "start",
          sortable: true,
        },
        { key: "stuId", title: "学号", value: "stuId" },
      ],

      thoughts: [
        {
          thought: "123",
          pictures: [],
        },
      ] as Thought[],

      dialog1: false,
      currentVol: undefined as VolunteerInfoResponse | undefined,
      currentThought: undefined as ThoughtInfoResponse | undefined,
      currentReward: NaN,
    };
  },
  mounted() {
    this.fetchThoughts();
  },
  methods: {
    fetchThoughts() {
      fApi.searchThoughts(
        undefined,
        ThoughtStatus.WaitingForFinalAudit
      )((result) => {
        this.thoughts = result;
      });
    },
    rowClick(
      event: Event,
      value: {
        item: any;
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
        if (status) {
          fApi.finalAudit(
            this.currentThought!.volId,
            this.currentThought!.stuId,
            this.currentReward
          )(() => {});
          this.fetchThoughts();
        } else {
          fApi.repulse(
            this.currentThought!.volId,
            this.currentThought!.stuId,
            ""
          )(() => {});
        }

        // validate(
        //   [this.currentReward],
        //   [validateNotNAN(), validateNotNegative(), validateNotLargerThan(4)]
        // );
      }
    },
  },
  computed: {
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
