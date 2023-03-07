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
            v-for="(item, index) in current.actions"
            :key="index"
            @click="item.onclick"
          />
        </v-card-actions>
      </v-card>
      <v-dialog v-model="uploadDlg" max-height="80%">
        <v-card>
          <v-card-title>上传感想</v-card-title>

          <v-form>
            <v-textarea v-model="current.thought!.thought" />
            <v-file-input v-model="current.picFiles">
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
        },
        {
          title: "名称",
          value: "name",
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
        vol: VolunteerInfoResponse;
        actions: {
          text: string;
          onclick: () => any;
        }[];
        thought: ThoughtInfoResponse | null;
        picFiles: File[];
      },

      infoDlg: false,
      thoughtDlg: false,
      uploadDlg: false,
    };
  },
  methods: {
    fetchVols() {
      fApi.searchVolunteers()((result) => {
        this.vols = result;
      });
    },
    onRowClick(ev: Event, v: any) {
      const item: SingleVolunteer = v.item.raw;
      fApi.getVolunteerInfo(item.id)((vol) => {
        this.current.vol = vol;
        if (
          vol.joiners.findIndex((v) => v.id == this.infoStore.userId) !== -1
        ) {
          fApi.getThoughtInfo(
            item.id,
            this.infoStore.userId
          )((thought) => {
            this.current.thought = thought;
            this.current.actions.push({
              text: "提交感想",
              onclick: () => {
                this.thoughtDlg = true;
              },
            });
          });
        } else {
          this.current.actions.push({
            text: "报名",
            onclick: () => {
              confirm("确定报名？").then(() => {
                fApi.signup(item.id, [this.infoStore.userId])(() => {});
              });
            },
          });
        }
        this.infoDlg = true;
      });
    },
    async saveThought() {
      const pics: {
        data: Uint8Array;
        name: string;
      }[] = [];
      for (const f of this.current.picFiles) {
        const readResult = await f.stream().getReader().read();
        if(!readResult.done){
          toasts.error(`文件${f.name}上传失败！`)
          continue;
        }
        pics.push({
          data: readResult.value??Uint8Array.from([]),
          name: f.name,
        });
      }
      fApi.saveThought(
        this.current.thought!.volId,
        this.current.thought!.stuId,
        this.current.thought!.thought,
        pics
      )(() => {});
    },
    async submitThought() {
      if (await confirm("确定提交？")) {
        fApi.submitThought(
          this.current.thought!.volId,
          this.current.thought!.stuId,
          this.current.thought!.thought,
          this.current.thought!.pictures
        );
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
