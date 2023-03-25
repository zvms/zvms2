<template>
  <v-container>
    <v-card>
      <v-card-title>
        未审核感想列表
        <v-btn @click="fetchThoughts" size="xsmall">
          <v-icon icon="mdi-reload" size="xsmall" />
        </v-btn>
      </v-card-title>
      <data-table
        fixed-header
        :headers="headers"
        :items="thoughts"
        @click:row="onRowClick"
        no-data-text="没有数据哦"
      />
    </v-card>
    <v-dialog v-model="dialog" persistent fullscreen scrollable>
      <v-card>
        <v-card-title>详细信息</v-card-title>
        <v-card-text>
          <vol-info v-if="currentVol" :vol="currentVol" />
          <thought-info
            v-if="currentThoughtData"
            :thought="currentThoughtData"
          />
          <v-spacer />
          发放的{{ getVolTypeName(currentVol!.type) }}时长（分钟）
          <v-text-field
            v-model="currentReward"
            prepend-icon="mdi-clock-time-three-outline"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn color="green" class="action" @click="audit(true)">通过 </v-btn>
          <v-btn color="red" class="action" @click="audit(false)">打回 </v-btn>
          <v-btn color="black" class="action" @click="dialog = false">
            关闭
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { confirm } from "@/utils/dialogs";
// import {
//   validate,
//   validateNotNAN,
//   validateNotLargerThan,
//   validateNotNegative,
// } from "@/utils/validation";
import {
  fApi,
  getVolTypeName,
  type VolunteerInfoResponse,
  type ThoughtInfoResponse,
  ThoughtStatus,
  type SingleThought,
  VolType,
  VolStatus,
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
          key: "volName",
          title: "义工名称",
          value: "volName",
          // align: "start",
          sortable: true,
        },
        {
          key: "stuName",
          title: "提交者",
          value: "stuName",
          // align: "start",
          sortable: true,
        },
        { key: "stuId", title: "学号", value: "stuId" },
      ],

      thoughts: [] as SingleThought[],

      dialog: false,
      currentVol: undefined as VolunteerInfoResponse | undefined,
      currentThoughtInfo: undefined as SingleThought | undefined,
      currentThoughtData: undefined as ThoughtInfoResponse | undefined,
      currentReward: NaN,
    };
  },
  mounted() {
    this.fetchThoughts();
  },
  methods: {
    fetchThoughts() {
      fApi.skipOkToast.searchThoughts({
        status: ThoughtStatus.WaitingForFinalAudit,
      })((result: SingleThought[]) => {
        this.thoughts = result;
      });
    },
    onRowClick(
      _event: Event,
      value: {
        item: any;
      }
    ) {
      const item = value.item.raw as SingleThought;
      this.currentThoughtInfo = item;
      fApi.skipOkToast.getVolunteerInfo(item.volId)((volunteer) => {
        fApi.skipOkToast.getThoughtInfo(
          item.volId,
          item.stuId
        )((thought) => {
          this.currentVol = volunteer;
          this.currentThoughtData = thought;
          this.currentReward = volunteer.reward;
          this.dialog = true;
        });
      });
    },
    /**
     * @param status `true` for ok.
     */
    async audit(status: boolean) {
      let value = await confirm();
      if (value) {
        if (status) {
          fApi.finalAudit(
            this.currentThoughtInfo!.volId,
            this.currentThoughtInfo!.stuId,
            this.currentReward
          )(() => {
            this.fetchThoughts();
            this.dialog = false;
          });
        } else {
          fApi.repulse(
            this.currentThoughtInfo!.volId,
            this.currentThoughtInfo!.stuId,
            ""
          )(() => {
            this.fetchThoughts();
            this.dialog = false;
          });
        }
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore),
  },
};
</script>

<style scoped>
.action {
  width: 30%;
  border: 1px solid currentColor;
}
</style>
