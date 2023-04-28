<template>
  <v-container>
    <v-card>
      <v-card-title>
        未审核感想列表
        <v-btn @click="fetchThoughts" size="xsmall">
          <v-icon icon="mdi-reload" size="xsmall" />
        </v-btn>
      </v-card-title>
      <v-container class="table-filter">
        <v-row>
          <v-col cols="8">
            <v-select
              x-small
              v-model="status"
              label="状态筛选"
              :items="
                [
                  ThoughtStatus.Accepted,
                  ThoughtStatus.Draft,
                  ThoughtStatus.WaitingForFinalAudit,
                ].map((v) => ({
                  name: getThoughtStatusName(v),
                  id: v,
                }))
              "
              item-title="name"
              item-value="id"
              prepend-icon="mdi-list-status"
              @update:model-value="fetchThoughts"
            />
          </v-col>
        </v-row>
      </v-container>
      <data-table
        fixed-header
        :headers="headers"
        :items="thoughts"
        @click:row="onRowClick"
      >
        <template v-slot:body v-if="thoughts.length === 0">
          <p class="text-center">是空的~</p>
        </template>
      </data-table>
    </v-card>
    <v-dialog v-model="dialog" persistent fullscreen scrollable>
      <v-card>
        <v-card-title>详细信息</v-card-title>
        <v-card-text>
          <vol-info v-if="currentVol" :vol="currentVol" />
          <thought-viewer
            v-if="currentThoughtData"
            :stu-name="currentThoughtInfo!.stuName"
            :thought="currentThoughtData"
            :showWordCount="true"
          />
          <v-spacer />
          发放的{{ getVolTypeName(currentVol!.type) }}时长（分钟）
          <v-text-field
            v-model.number="currentReward"
            type="text"
            prepend-icon="mdi-clock-time-three-outline"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn color="green" class="action" @click.prevent="audit(true)"
            >通过
          </v-btn>
          <v-btn color="red" class="action" @click.prevent="audit(false)"
            >打回
          </v-btn>
          <v-btn color="black" class="action" @click.prevent="dialog = false">
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
  getThoughtStatusName,
} from "@/apis";
import { useInfoStore } from "@/stores";
import { timeToHint } from "@/utils/calc";
import { mapStores } from "pinia";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";
import ThoughtViewer from "@/components/thought/viewer.vue";
import VolInfo from "@/components/vol-info.vue";

export default {
  components: {
    DataTable,
    VolInfo,
    ThoughtViewer,
  },
  data() {
    return {
      timeToHint,
      getVolTypeName,
      ThoughtStatus,
      getThoughtStatusName,
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
      status: ThoughtStatus.WaitingForFinalAudit,
    };
  },
  beforeMount() {
    this.fetchThoughts();
  },
  methods: {
    fetchThoughts() {
      //
      fApi.skipOkToast.searchThoughts({
        status: this.status,
        /*status: ThoughtStatus.WaitingForFinalAudit,*/
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
      if (await confirm()) {
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
          fApi.repulseThought(
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
