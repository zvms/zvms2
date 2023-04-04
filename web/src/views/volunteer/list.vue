<template>
  <v-container>
    <v-card>
      <v-card-title>
        义工列表
        <v-btn @click="fetchVols" size="xsmall">
          <v-icon icon="mdi-reload" size="xsmall" />
        </v-btn>
      </v-card-title>
      <v-container>
        <v-row>
          <v-select
            v-if="
              infoStore.permission &
              (Categ.Manager | Categ.Auditor | Categ.System)
            "
            x-small
            prepend-icon="mdi-account-group"
            v-model="filter.class"
            label="限定班级"
            :items="classes"
            item-title="name"
            item-value="id"
            class="pl-5 pr-20"
          />
        </v-row>
      </v-container>
      <data-table
        fixed-header
        :headers="headers"
        :items="volsForTable"
        @click:row="onRowClick"
      >
        <template v-slot:body v-if="vols.length === 0">
          <p class="text-center">是空的~</p>
        </template>
      </data-table>
    </v-card>
    <v-dialog v-if="infoDlg" v-model="infoDlg" persistent fullscreen scrollable>
      <v-card>
        <v-card-title variant="outlined">{{ current.vol.name }}</v-card-title>

        <v-card-text>
          <vol-info :vol="current.vol" class="pa-14" />
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
          <v-card-title outlined>上传感想</v-card-title>
          <v-card-text>
            <v-form>
              <v-textarea
                v-model="current.thought!.data.thought"
                label="感想文字"
              />
              <v-file-input
                accept="image/*"
                @update:model-value="uploadImg"
                label="感想图片，支持拖入"
              >
                <!-- <template v-slot:selection="{ fileNames }">
                <template v-for="fileName in fileNames" :key="fileName">
                  <v-img :src="fileName" />
                </template>
              </template> -->
              </v-file-input>
              <v-container>
                <v-row>
                  <v-col v-for="p,i in current.thought!.pics" :key="p.key">
                    <v-img
                      :src="`data:${p.type};base64,${p.base64}`"
                      max-width="10em"
                      outlined
                    />
                    <v-btn
                      color="white"
                      @click="current.thought!.pics.splice(i, 1)"
                      >删除</v-btn
                    >
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
  </v-container>
</template>

<script lang="ts">
import { confirm, toasts } from "@/utils/dialogs.js";
import { Categ } from "@/apis/types/enums";
import VolInfo from "@/components/vol-info.vue";
import {
  fApi,
  VolStatus,
  type SingleClass,
  type SingleVolunteer,
  type ThoughtInfoResponse,
  type VolunteerInfoResponse,
  getVolStatusName
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
      getVolStatusName,
      Categ,
      headers: [
        {
          title: "名称",
          value: "name",
          key: "name",
        },
        {
          title: "时间",
          value: "time",
          key: "time",
        },
        {
          title: "状态",
          value: "status",
          key: "status",
        },
      ],
      vols: [] as SingleVolunteer[],
      filter: {
        class: -1 /** any */,
      },
      classes: [] as SingleClass[],
      current: undefined as any as {
        singleVol: SingleVolunteer;
        vol: VolunteerInfoResponse;
        thought?: {
          data: ThoughtInfoResponse;
          pics: {
            type: string;
            extName: string;
            base64: string;
            key: string;
          }[];
        };
      },

      infoDlg: false,
      thoughtDlg: false,
    };
  },
  mounted() {
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
      fApi.skipOkToast.searchVolunteers({
        student:
          this.infoStore.permission &
          (Categ.Class |
            Categ.Manager |
            Categ.Teacher |
            Categ.System |
            Categ.Auditor)
            ? undefined
            : this.infoStore.userId,
        cls:
          this.infoStore.permission &
          (Categ.Manager | Categ.System | Categ.Auditor)
            ? this.filter.class === -1
              ? undefined
              : this.filter.class
            : this.infoStore.classId,
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
      fApi.getThoughtInfo(
        this.current!.singleVol.id,
        this.infoStore.userId
      )((thought) => {
        this.current.thought = { data: thought, pics: [] };
      });
    },
    async uploadImg(files: File[]) {
      const newFile = files[0];
      if (newFile.size > 1024 * 1024 * 10) {
        toasts.error("图片大小不能超过10MB");
        return;
      }
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
        extName: newFile.name.substring(newFile.name.lastIndexOf(".") + 1),
        base64: CryptoJS.enc.Base64.stringify(
          ArrayBufferToWordArray(arrayBuffer)
        ),
        key: Date.now() + "",
      });
    },
    async saveThought(then = () => {}) {
      fApi.saveThought(
        this.current.singleVol.id,
        this.infoStore.userId,
        this.current.thought!.data.thought ?? "",
        this.current.thought!.pics.map((v) => ({
          type: v.type,
          base64: v.base64,
        }))
      )(then);
    },
    async submitThought() {
      // this.saveThought(async () => {
      //   if (await confirm("确定提交？")) {
      //     fApi.submitThought(
      //       this.current.thought!.volId,
      //       this.current.thought!.stuId
      //     );
      //   }
      // });
      if (await confirm("确定提交？")) {
        fApi.submitThought(
          this.current.singleVol.id,
          this.infoStore.userId,
          this.current.thought!.data.thought ?? "",
          this.current.thought!.pics.map((v) => ({
            type: v.extName,
            base64: v.base64,
          }))
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
        (this.infoStore.permission & Categ.Class) |
          Categ.Teacher |
          Categ.System &&
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
      return result;
    },
    volsForTable(){
      return this.vols.map(
        vol=>({
          ...vol,
          status: this.getVolStatusName(vol.status),
        })
      )
    }
  },
  watch: {
    // "filter.class"(v: number[], ov: number[]) {
    //   if (v.indexOf(-1) !== -1) {
    //     if (ov.indexOf(-1) === -1) {
    //       console.log("1");
    //       this.filter.class = [-1];
    //     } else {
    //       console.log("2");
    //       this.filter.class.splice(v.indexOf(-1));
    //     }
    //   }
    // },
    "filter.class"() {
      this.fetchVols();
    },
  },
};
</script>
