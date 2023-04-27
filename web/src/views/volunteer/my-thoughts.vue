<template>
  <v-container>
    <v-card>
      <v-card-title>
        我的感想
        <v-btn @click="fetchThoughts" size="xsmall">
          <v-icon icon="mdi-reload" size="xsmall" />
        </v-btn>
      </v-card-title>
      <v-container class="pb-0">
        <v-row>
          <v-select
            v-model="filter.status"
            label="筛选状态"
            :items="statusSelectorItems"
            item-title="name"
            item-value="id"
            class="pl-5 pr-20"
          />
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
        <template v-slot:item.status="{ item }">
          <v-chip label :color="getThoughtStatusDisplayColor(item.raw.status)">
            {{ getThoughtStatusName(item.raw.status) }}
          </v-chip>
        </template>
      </data-table>
    </v-card>
    <v-dialog v-model="thoughtDlg" persistent fullscreen>
      <ThoughtEditor
        :stuName="infoStore.username"
        :volId="currentVolId"
        :vol="currentVol"
        :stuId="currentThoughtStuId"
        :thought="currentThought"
        @close="
          fetchThoughts();
          thoughtDlg = false;
        "
      />
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import {
  ThoughtStatus,
  fApi,
  getThoughtStatusName,
  type ThoughtInfoResponse,
  type VolunteerInfoResponse,
  type SingleThought,
} from "@/apis";
import { Categ } from "@/apis/types/enums";
import { useInfoStore } from "@/stores";
import { mapStores } from "pinia";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";
import ThoughtEditor from "@/components/thought/editor.vue";
import { getThoughtStatusDisplayColor } from "@/utils/calc";

export default {
  components: {
    DataTable,
    ThoughtEditor,
  },
  data() {
    return {
      Categ,
      getThoughtStatusName,
      getThoughtStatusDisplayColor,
      ThoughtStatus,
      headers: [
        {
          title: "义工名称",
          value: "volName",
          key: "volName",
        },
        {
          title: "状态",
          key: "status",
        },
        {
          title: "进行时间",
          value: "volTime",
          key: "volTime",
        },
      ],
      thoughts: [] as SingleThought[],
      filter: {
        status: -1 /** any */ as ThoughtStatus | -1,
      },
      currentVolId: NaN,
      currentVol: undefined as any as VolunteerInfoResponse,
      currentThoughtStuId: NaN,
      currentThought: undefined as any as ThoughtInfoResponse,
      thoughtDlg: false,
    };
  },
  beforeMount() {
    this.fetchThoughts();
  },
  methods: {
    resetFilter() {
      this.filter.status = -1;
    },
    fetchThoughts() {
      fApi.skipOkToast.listStudentThoughts(this.infoStore.userId, {
        status: this.filter.status == -1 ? undefined : this.filter.status,
      })((result) => {
        this.thoughts = result;
      });
    },
    onRowClick(_ev: Event, v: any) {
      const item: SingleThought = v.item.raw;
      fApi.skipOkToast.getThoughtInfo(
        item.volId,
        item.stuId
      )((thought) => {
        this.currentThoughtStuId = item.stuId;
        this.currentThought = thought;
        fApi.skipOkToast.getVolunteerInfo(item.volId)((vol) => {
          this.currentVolId = item.volId;
          this.currentVol = vol;
          this.thoughtDlg = true;
        });
      });
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    statusSelectorItems() {
      return [
        {
          id: -1,
          name: "查看全部",
        },
        ...[
          ThoughtStatus.Draft,
          ThoughtStatus.WaitingForFinalAudit,
          ThoughtStatus.Accepted,
        ].map((v) => ({
          id: v,
          name: getThoughtStatusName(v),
        })),
      ];
    },
  },
  watch: {
    "filter.status"() {
      this.fetchThoughts();
    },
  },
};
</script>
<style scoped>
.v-card-actions {
  margin-left: 1.5em;
  margin-bottom: 1em;
}

.v-card-actions > button {
  min-width: 7em;
  font-size: x-large;
  border: solid 1px currentColor;
}

.disabled-input {
  pointer-events: none;
}

.divider {
  width: 100%;
  border-bottom: 1px grey solid;
  height: 1px;
}
</style>
