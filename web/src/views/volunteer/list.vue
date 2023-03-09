<template>
  <v-container>
    <v-card color="primary" dark>
      <v-card-title>
        义工列表
        <v-spacer></v-spacer>
      </v-card-title>
    </v-card>
    <data-table
      fixed-header
      :headers="headers"
      :items="vols"
      no-data-text="没有数据哦"
      no-results-text="没有结果"
      @click:row="onRowClick"
    >
    </data-table>

    <v-dialog v-model="infoDlg" max-width="80%">
      <v-card>
        <v-card-title></v-card-title>

        <v-card-actions>
          <v-btn
            v-for="(item, index) in actions"
            :key="index"
            @click="item.onclick"
          />
        </v-card-actions>
      </v-card>
      <v-dialog v-model="uploadDlg" max-height="80%">
        <v-card>
          <v-card-title>上传感想</v-card-title>

          <v-form>
            <v-textarea v-model="current.thought!.data.thought" />
            <v-file-input v-model="current.thought!.picFiles">
              <template v-slot:selection="{ fileNames }">
                <template v-for="fileName in fileNames" :key="fileName">
                  <v-img :src="fileName" />
                </template>
              </template>
            </v-file-input>
          </v-form>
          <v-card-actions>
            <v-btn @click="saveThought">保存</v-btn>
            <v-btn @click="submitThought">提交</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { confirm, toasts } from "@/utils/dialogs.js";
import { permissionTypes } from "@/utils/permissions";
import volinfo from "@/components/vol-info.vue";
import {
  fApi,
  VolStatus,
  type SingleVolunteer,
  type Thought,
  type ThoughtInfoResponse,
  type VolunteerInfoResponse,
} from "@/apis";
import { useInfoStore } from "@/stores";
import { mapStores } from "pinia";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";
import Base64 from "crypto-js/enc-base64";

interface Action {
  text: string;
  onclick: () => any;
}

export default {
  components: {
    volinfo,
    DataTable,
  },
  data() {
    return {
      headers: [
        {
          title: "编号",
          value: "id",
          key: "id",
        },
        {
          title: "名称",
          value: "name",
          key: "name",
        },
      ],
      vols: [
        {
          id: 12211,
          name: "111",
          time: "11",
          status: 11,
        },
        {
          id: 12211,
          name: "111",
          time: "11",
          status: 11,
        },
      ] as SingleVolunteer[],

      current: undefined as any as {
        singleVol: SingleVolunteer;
        vol: VolunteerInfoResponse;
        thought?: {
          data: ThoughtInfoResponse;
          picFiles: File[];
        };
      },

      infoDlg: false,
      thoughtDlg: false,
      uploadDlg: false,
    };
  },
  methods: {
    fetchVols() {
      fApi.searchVolunteers({
        student:
          this.infoStore.permission &
          (permissionTypes.secretary | permissionTypes.teacher)
            ? undefined
            : this.infoStore.userId,
        cls:
          this.infoStore.permission & permissionTypes.system
            ? undefined
            : this.infoStore.classId,
      })((result) => {
        this.vols = result;
      });
    },

    onRowClick(ev: Event, v: any) {
      const item: SingleVolunteer = v.item.raw;
      fApi.getVolunteerInfo(item.id)((vol) => {
        this.current = {
          singleVol: item,
          vol,
        };
        this.infoDlg = true;
      });
    },
    viewThought() {
      fApi.getThoughtInfo(
        this.current!.singleVol.id,
        this.infoStore.userId
      )((thought) => {
        this.current.thought = { data: thought, picFiles: [] };
      });
    },
    async saveThought() {
      const pics: string[] = [];
      for (const f of this.current.thought!.picFiles) {
        const readResult = await f.stream().getReader().read();
        if (!readResult.done) {
          toasts.error(`文件${f.name}上传失败！`);
          continue;
        }
        pics.push(Base64.stringify(readResult.value ?? Uint8Array.from([])));
      }
      fApi.saveThought(
        this.current.singleVol.id,
        this.infoStore.userId,
        this.current.thought!.data.thought ?? "",
        pics
      )(() => {});
    },
    async submitThought() {
      this.saveThought();
      if (await confirm("确定提交？")) {
        fApi.submitThought(
          this.current.thought!.volId,
          this.current.thought!.stuId
        );
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    actions(): Action[] {
      let result: Action[] = [];
      if (
        this.current!.vol.joiners.findIndex(
          (v) => v.id === this.infoStore.userId
        ) > -1
      ) {
        result.push({
          text: "感想",
          onclick: () => {
            this.thoughtDlg = true;
          },
        });
      }
      if (this.current.vol.signable) {
        result.push({
          text: "报名",
          onclick: () => {
            confirm("确定报名？").then(() => {
              fApi.signup(this.current.singleVol.id, [this.infoStore.userId])(
                () => {}
              );
            });
          },
        });
      }
      return result;
    },
  },
};
</script>
