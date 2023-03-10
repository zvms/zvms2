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
      <v-dialog v-model="thoughtDlg" max-height="80%">
        <v-card>
          <v-card-title>上传感想</v-card-title>

          <v-form>
            <v-textarea v-model="current.thought!.data.thought" />
            <v-file-input accept="image/*" @update:model-value="uploadImg">
              <!-- <template v-slot:selection="{ fileNames }">
                <template v-for="fileName in fileNames" :key="fileName">
                  <v-img :src="fileName" />
                </template>
              </template> -->
            </v-file-input>
            <v-container>
              <v-row>
                <v-col v-for="p,i in current.thought!.pics" :key="i">
                  <v-img :src="`data:${p.type};base64,${p.base64}`" />
                </v-col>
              </v-row>
            </v-container>
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
          pics: {
            type: string;
            base64: string;
          }[];
        };
      },

      infoDlg: false,
      thoughtDlg: false,
    };
  },
  mounted() {
    this.fetchVols();
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
        this.current.thought = { data: thought, pics: [] };
      });
    },
    async uploadImg(files: File[]) {
      const newFile = files[0];
      const readResult = await newFile.stream().getReader().read();
      if (!readResult.done) {
        toasts.error(`文件${newFile.name}上传失败！`);
        return;
      }
      this.current.thought!.pics.push({
        type: newFile.type,
        base64: Base64.stringify(readResult.value ?? Uint8Array.from([])),
      });
    },
    async saveThought(then = () => {}) {
      fApi.saveThought(
        this.current.singleVol.id,
        this.infoStore.userId,
        this.current.thought!.data.thought ?? "",
        this.current.thought!.pics.map((v) => v.base64)
      )(then);
    },
    async submitThought() {
      this.saveThought(async () => {
        if (await confirm("确定提交？")) {
          fApi.submitThought(
            this.current.thought!.volId,
            this.current.thought!.stuId
          );
        }
      });
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
