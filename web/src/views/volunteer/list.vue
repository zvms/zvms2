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

    <v-dialog v-if="infoDlg" v-model="infoDlg" persistent fullscreen scrollable>
      <v-card>
        <v-card-title>{{ current.vol.name }}</v-card-title>

        <v-card-text>
          <vol-info :vol="current.vol" />
        </v-card-text>

        <v-card-actions>
          <v-btn
            v-for="(item, index) in actions"
            :key="index"
            @click="item.onclick"
            >{{ item.text }}</v-btn
          >
        </v-card-actions>
      </v-card>
      <v-dialog v-model="thoughtDlg" persistent fullscreen>
        <v-card>
          <v-card-title>上传感想</v-card-title>
          <v-card-text>
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
                    <v-img :src="`data:${p.type};base64,${p.base64}`" class="m-10" max-width="10em" outlined/>
                    <v-btn color="white" @click="current.thought!.pics.splice(i)">删除</v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="saveThought">保存</v-btn>
            <v-btn @click="submitThought">提交</v-btn>
            <v-btn @click="thoughtDlg = false">关闭</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-dialog>
    <v-btn @click="test">test</v-btn>
  </v-container>
</template>

<script lang="ts">
import { confirm, toasts } from "@/utils/dialogs.js";
import { permissionTypes } from "@/utils/permissions";
import VolInfo from "@/components/vol-info.vue";
import {
  fApi,
  VolStatus,
  type SingleVolunteer,
  type Thought,
  type ThoughtInfoResponse,
  type VolunteerInfoResponse,
  VolType,
} from "@/apis";
import { useInfoStore } from "@/stores";
import { mapStores } from "pinia";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";
import CryptoJS from "crypto-js";

interface Action {
  text: string;
  onclick: () => any;
}

export default {
  components: {
    VolInfo,
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
    test() {
      this.current = {
        singleVol: this.vols[0],
        vol: {
          name: "VolName",
          description: "DESC",
          time: "1-1-1",
          status: VolStatus.Unaudited,
          type: VolType.Inside,
          reward: 111,
          signable: true,
          joiners: [
            {
              id: 1,
              name: "abc",
            },
          ],
          holder: 2,
          holderName: "aaa",
        },
        thought: {
          data: {
            thought: "thought text",
            pics: ["1111", "1111"],
          },
          pics: [],
        },
      };
      this.infoDlg = true;
      this.thoughtDlg = true;
    },
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
      const arrayBuffer = await newFile.arrayBuffer();
      if (!arrayBuffer) {
        toasts.error(`文件${newFile.name}上传失败！`);
        return;
      }
      function ArrayBufferToWordArray(arrayBuffer: ArrayBuffer | Uint8Array) {
        let u8: Uint8Array;
        if (arrayBuffer instanceof ArrayBuffer)
          u8 = new Uint8Array(arrayBuffer, 0, arrayBuffer.byteLength);
        else u8 = arrayBuffer;
        const len = u8.length;
        const words: any[] = [];
        for (let i = 0; i < len; i += 1) {
          words[i >>> 2] |= (u8[i] & 0xff) << (24 - (i % 4) * 8);
        }
        return CryptoJS.lib.WordArray.create(words, len);
      }
      this.current.thought!.pics.push({
        type: newFile.type,
        base64: CryptoJS.enc.Base64.stringify(
          ArrayBufferToWordArray(arrayBuffer)
        ),
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
            confirm("确定报名？").then((ok) => {
              if (ok) {
                fApi.signup(this.current.singleVol.id, [
                  this.infoStore.userId,
                ])();
              }
            });
          },
        });
      }
      if (
        (this.infoStore.permission & permissionTypes.secretary) |
          permissionTypes.teacher |
          permissionTypes.system &&
        this.current.vol.status === VolStatus.Unaudited
      ) {
        result.push({
          text: "允许报名",
          onclick: () => {
            confirm("确定？").then((ok) => {
              if (ok) {
                fApi.auditVolunteer(this.current.singleVol.id)();
              }
            });
          },
        });
      }
      result.push({
        text: "关闭",
        onclick: () => {
          this.infoDlg = false;
        },
      });
      result.push({
        text: "test",
        onclick: () => {},
      });
      return result;
    },
  },
};
</script>
