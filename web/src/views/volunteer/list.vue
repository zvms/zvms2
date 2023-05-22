<template>
  <v-card>
    <v-card-title class="pt-0">
      <v-container style="margin-bottom: -30px">
        <v-row>
          <v-col cols="4" class="pl-3 ma-0">
            义工列表
            <v-btn @click="fetchVols" size="xsmall">
              <v-icon icon="mdi-reload" size="xsmall" />
            </v-btn>
          </v-col>
          <v-col cols="4" class="pa-0 ma-0 h-50">
            <v-select
              v-model="filter.status"
              label="筛选状态"
              :items="statusSelectorItems"
              prepend-icon="mdi-list-status"
              item-title="name"
              item-value="id"
            />
          </v-col>
          <v-col cols="4" class="py-0 ma-0">
            <v-select
              v-if="
                infoStore.permission &
                (Categ.Manager | Categ.Auditor | Categ.System)
              "
              prepend-icon="mdi-account-multiple"
              v-model="filter.class"
              label="限定班级"
              :items="classes"
              item-title="name"
              item-value="id"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-card-title>
    <data-table
      fixed-header
      :headers="headers"
      :items="volsForTable"
      @click:row="onRowClick"
    >
      <template v-slot:body v-if="vols.length === 0">
        <table-placeholder />
      </template>
      <template v-slot:item.name="{ item }">
        <div class="vol-name-in-table">
          {{ item.raw.name }}
        </div>
      </template>
      <template v-slot:item.status="{ item }">
        <v-chip label :color="item.raw.statusColor">
          {{ item.raw.statusText }}
        </v-chip>
      </template>
    </data-table>
  </v-card>
  <v-dialog v-if="infoDlg" v-model="infoDlg" persistent fullscreen scrollable>
    <v-card>
      <v-card-title variant="outlined">
        义工 {{ current.vol.name }} 的详细信息
      </v-card-title>

      <v-card-text>
        <vol-info
          :vol-id="current.singleVol.id"
          :vol="current.vol"
          :signup-rollupable="signupRollupable"
          class="pa-14"
        />
      </v-card-text>
      <v-dialog v-if="modDlg" v-model="modDlg">
        <v-card-text>
          <vol-modify :volId="current.singleVol.id" />
        </v-card-text>
      </v-dialog>

      <v-card-actions>
        <v-btn
          v-for="(item, index) in actions"
          :key="index"
          @click="item.onclick"
        >
          {{ item.text }}
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-dialog v-model="thoughtDlg" persistent fullscreen>
      <ThoughtEditor
        :stuName="infoStore.username"
        :volId="current.singleVol.id"
        :vol="current.vol"
        :stuId="infoStore.userId"
        :thought="current.thought!!"
        @close="thoughtDlg = false"
      />
    </v-dialog>
  </v-dialog>
</template>

<script lang="ts">
import {
  ThoughtStatus,
  VolStatus,
  fApi,
  getThoughtStatusName,
  type SingleClass,
  type SingleVolunteer,
  type ThoughtInfoResponse,
  type VolunteerInfoResponse,
} from "@/apis";
import { Categ, getVolStatusName } from "@/apis/types/enums";
import VolInfo from "@/components/vol/vol-info.vue";
import { useInfoStore, useLoadingStore } from "@/stores";
import { getVolStatusDisplayText } from "@/utils/calc";
import { confirm } from "@/utils/dialogs";
import { mapStores } from "pinia";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";
import ThoughtEditor from "@/components/thought/editor.vue";
import TablePlaceholder from "@/components/table-placeholder.vue";
import VolModify from "@/components/vol/vol-modify.vue";

interface Action {
  text: string;
  onclick: () => any;
}

export default {
  components: {
    VolModify,
    VolInfo,
    DataTable,
    ThoughtEditor,
    TablePlaceholder,
  },
  data() {
    return {
      Categ,
      getThoughtStatusName,
      ThoughtStatus,
      headers: [
        {
          title: "名称",
          value: "name",
          key: "name",
          width: 430,
        },
        {
          title: "创建者",
          value: "holderName",
          key: "holderName",
          width: 120,
        },
        {
          title: "状态",
          key: "status",
          width: 150,
        },
        {
          title: "预期进行时间",
          value: "time",
          key: "time",
          width: 230,
        },
      ],
      vols: [] as SingleVolunteer[],
      filter: {
        status: -1 /** any */ as VolStatus | -1,
        class: -1 /** any */,
      },
      classes: [] as SingleClass[],
      current: undefined as any as {
        singleVol: SingleVolunteer;
        vol: VolunteerInfoResponse;
        thought?: ThoughtInfoResponse;
      },
      picsId: "",
      infoDlg: false,
      thoughtDlg: false,
      tab: "one",
      modDlg: false,
    };
  },
  beforeMount() {
    fApi.skipOkToast.listClasses()((classes) => {
      this.classes = [
        {
          id: -1,
          name: "任意班级",
        },
        ...classes,
      ];
    });
    this.fetchVols();
  },
  methods: {
    resetFilter() {
      this.filter.class = -1;
    },
    fetchVols() {
      this.infoDlg = false;
      this.thoughtDlg = false;
      fApi.skipOkToast.listVolunteers({
        cls:
          this.infoStore.permission &
            (Categ.Manager | Categ.System | Categ.Auditor) &&
          this.filter.class !== -1
            ? this.filter.class
            : undefined,
      })((result) => {
        this.vols = result;
      });
    },
    onRowClick(ev: Event, v: any) {
      const item: SingleVolunteer = v.item.raw;
      fApi.skipOkToast.getVolunteerInfo(item.id)((vol) => {
        this.current = {
          singleVol: item,
          vol,
        };
        this.infoDlg = true;
      });
    },
    viewThought() {
      fApi.skipOkToast.getThoughtInfo(
        this.current!.singleVol.id,
        this.infoStore.userId
      )((thought) => {
        this.current.thought = thought;
        this.thoughtDlg = true;
      });
    },
  },
  computed: {
    ...mapStores(useInfoStore, useLoadingStore),
    isJoiner() {
      return (
        this.current!.vol.joiners.findIndex(
          (v) => v.id === this.infoStore.userId
        ) !== -1
      );
    },
    actions(): Action[] {
      let result: Action[] = [];
      if (this.isJoiner) {
        result.push({
          text: "查看/修改感想",
          onclick: () => {
            this.viewThought();
          },
        });
      }
      if (
        !this.isJoiner &&
        this.current.vol.signable &&
        this.current.vol.status === VolStatus.Audited &&
        this.infoStore.permission & Categ.Student
      ) {
        result.push({
          text: "报名",
          onclick: async () => {
            if (await confirm("确定报名？")) {
              fApi.signup(this.current.singleVol.id, [this.infoStore.userId])(
                () => {
                  this.fetchVols();
                }
              );
            }
          },
        });
      }
      if (
        this.infoStore.permission &
          (Categ.Class | Categ.Teacher | Categ.System) &&
        this.current.vol.status === VolStatus.Unaudited
      ) {
        result.push({
          text: "允许报名",
          onclick: async () => {
            if (await confirm("确定？")) {
              fApi.auditVolunteer(this.current.singleVol.id)(() => {
                this.fetchVols();
              });
            }
          },
        });
        result.push({
          text: "禁止报名",
          onclick: async () => {
            if (await confirm("确定？")) {
              fApi.repulseVolunteer(this.current.singleVol.id)(() => {
                this.fetchVols();
              });
            }
          },
        });
      }
      result.push({
        text: "关闭",
        onclick: () => {
          this.infoDlg = false;
        },
      });
      return result;
    },
    volsForTable() {
      return this.vols
        .map((vol) => ({
          ...vol,
          statusText: getVolStatusDisplayText(this.infoStore.userId, vol)[0],
          statusColor: getVolStatusDisplayText(this.infoStore.userId, vol)[1],
        }))
        .filter(
          (v) => this.filter.status === -1 || v.status === this.filter.status
        );
    },
    statusSelectorItems() {
      return [
        {
          id: -1,
          name: "查看全部",
        },
        ...[
          VolStatus.Unaudited,
          VolStatus.Audited,
          VolStatus.Rejected,
          VolStatus.Finished,
          VolStatus.Deprecated,
        ].map((v) => ({
          id: v,
          name: getVolStatusName(v),
        })),
      ];
    },
    signupRollupable(): boolean {
      const enoughPermission = Boolean(
        this.infoStore.permission & (Categ.Manager | Categ.System)
      );
      const isHolder = this.infoStore.userId === this.current!.vol!.holder;
      const isThisClassSecretary = false; // (this.infoStore.permission&Categ.Class)&&this.currentVol!.joiners[0]..??;
      return enoughPermission || isHolder || isThisClassSecretary;
    },
  },
  watch: {
    "filter.class"() {
      this.fetchVols();
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
