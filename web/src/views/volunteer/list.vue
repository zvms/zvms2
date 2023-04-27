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
        <template v-slot:item.status="{ item }">
          <v-chip label :color="item.raw.statusColor">
            {{ item.raw.statusText }}
          </v-chip>
        </template>
      </data-table>
    </v-card>
    <v-dialog v-if="infoDlg" v-model="infoDlg" persistent fullscreen scrollable>
      <v-card>
        <v-card-title variant="outlined"
          >义工 {{ current.vol.name }} 的详细信息</v-card-title
        >

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
          <v-card-title> 您在义工 {{ current.vol.name }} 的感想 </v-card-title>
          <v-card-text>
            感想状态：
            <br />
            <strong style="font-size: larger">
              {{ getThoughtStatusName(current.thought!.data.status) }}
            </strong>
            <span v-if="current.thought!.data.status===ThoughtStatus.Accepted">
              时长{{ current.thought!.data.reward }}分钟
            </span>
            <span v-if="current.thought!.data.reason">
              上次的提交被打回的原因：
              <br />
              {{ current.thought!.data.reason }}
            </span>
            <div class="my-3"></div>
            <v-form>
              <markdown-editor
                v-if="isThoughtModifiable"
                v-model="current.thought!.data.thought"
              />
              <markdown-viewer
                v-else
                :markdown="current.thought!.data.thought"
                label="感想文字"
              />
              <div class="my-3 divider"></div>
              感想图片
              <v-tabs v-if="isThoughtModifiable" v-model="tab">
                <v-tab value="one"> 通过图片ID上传 </v-tab>
                <v-tab value="two"> 从本地上传（学海平板无效） </v-tab>
              </v-tabs>
              <v-window v-if="isThoughtModifiable" v-model="tab">
                <v-window-item value="one">
                  <v-text-field label="图片ID" v-model="picsId" />
                  <v-btn @click="uploadFromId" style="border: 1px gray solid">
                    上传
                  </v-btn>
                </v-window-item>
                <v-window-item value="two">
                  <v-file-input
                    accept="image/*"
                    @update:model-value="uploadImg"
                    label="感想图片，支持拖入"
                  />
                </v-window-item>
              </v-window>

              <v-img :src="test" />
              <v-container>
                <v-row>
                  <v-col v-for="p,i in current.thought!.pics" :key="p.key">
                    <v-img
                      :src="
                        p.byHash ? p.url : `data:${p.type};base64,${p.base64}`
                      "
                      max-width="10em"
                      outlined
                    />
                    <v-btn
                      v-if="isThoughtModifiable"
                      color="white"
                      @click="current.thought!.pics.splice(i, 1)"
                    >
                      删除
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn v-if="isThoughtModifiable" @click="submitThought"
              >提交</v-btn
            >
            <v-btn @click="maySaveThoughtAndClose"
              >{{ isThoughtModifiable ? "保存并" : "" }}关闭</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-dialog>
  </v-container>
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
  type Picture,
} from "@/apis";
import { Categ } from "@/apis/types/enums";
import MarkdownEditor from "@/components/markdown/editor.vue";
import MarkdownViewer from "@/components/markdown/viewer.vue";
import VolInfo from "@/components/vol-info.vue";
import { baseURL } from "@/plugins/axios";
import { useInfoStore } from "@/stores";
import { getVolStatusDisplayForUser } from "@/utils/calc";
import { confirm, toasts } from "@/utils/dialogs";
import { ArrayBufferToWordArray, getPicsById } from "@/utils/pics";
import { resumeScroll, saveScroll } from "@/utils/scrollCtrl";
import CryptoJS from "crypto-js";
import { mapStores } from "pinia";
import { VDataTable as DataTable } from "vuetify/labs/VDataTable";

interface Action {
  text: string;
  onclick: () => any;
}

export default {
  components: {
    VolInfo,
    DataTable,
    MarkdownEditor,
    MarkdownViewer,
  },
  data() {
    return {
      test: "",
      Categ,
      getThoughtStatusName,
      ThoughtStatus,
      headers: [
        {
          title: "名称",
          value: "name",
          key: "name",
        },
        {
          title: "创建者",
          value: "holderName",
          key: "holderName",
        },
        {
          title: "状态",
          key: "status",
        },
        {
          title: "进行时间",
          value: "time",
          key: "time",
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
          pics: (
            | {
                byHash: false;
                type: string;
                extName: string;
                base64: string;
                key: string;
              }
            | {
                byHash: true;
                hash: string;
                type: string;
                url: string;
                key: string;
              }
          )[];
        };
      },
      picsId: "",
      infoDlg: false,
      thoughtDlg: false,
      tab: "one",
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
        this.current.thought = {
          data: thought,
          pics:
            thought.pics?.map((v) => ({
              byHash: true,
              hash: v.hash,
              type: v.type,
              url: `${baseURL}/static/pics/${v.hash}.${v.type}`,
              key: v.hash,
            })) ?? [],
        };
        this.thoughtDlg = true;
      });
    },
    async uploadFromId() {
      if (Number.isNaN(parseInt(this.picsId, 36))) {
        toasts.error("图片ID格式错误");
        return;
      }
      try {
        const pics = await getPicsById(this.picsId);

        if (pics.length === 0) {
          toasts.error("图片不存在");
          return;
        }
        for (const pic of pics) {
          fApi.fetchPicture(
            this.current.singleVol.id,
            this.infoStore.userId,
            pic
          )((result) => {
            this.current.thought!.pics.push({
              byHash: true,
              hash: result.hash,
              type: result.type,
              url: `${baseURL}/static/pics/${result.hash}.${result.type}`,
              key: result.hash,
            });
          });
        }
        this.picsId = "";
      } catch (err: any) {
        toasts.error("通过ID获取图床图片失败! " + err?.message);
      }
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
      this.current.thought!.pics.push({
        byHash: false,
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
        await this.picsForUpload
      )(then);
    },
    async submitThought() {
      if (await confirm("确定提交？提交后不可修改！")) {
        fApi.submitThought(
          this.current.singleVol.id,
          this.infoStore.userId,
          this.current.thought!.data.thought ?? "",
          await this.picsForUpload
        )(() => {
          this.thoughtDlg = false;
        });
      }
    },
    async maySaveThoughtAndClose() {
      if (this.isThoughtModifiable) {
        this.saveThought(() => {
          this.thoughtDlg = false;
        });
      } else {
        this.thoughtDlg = false;
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore),
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
      return this.vols.map((vol) => ({
        ...vol,
        statusText: getVolStatusDisplayForUser(this.infoStore.userId, vol)[0],
        statusColor: getVolStatusDisplayForUser(this.infoStore.userId, vol)[1],
      }));
    },
    async picsForUpload() {
      try {
        const pics: Picture[] = [];
        for (const v of this.current.thought!.pics) {
          if (v.byHash) {
            pics.push({
              type: v.type,
              hash: v.hash,
            });
          } else {
            pics.push({
              type: v.extName,
              base64: v.base64,
            });
          }
        }
        return pics;
      } catch (e: any) {
        toasts.error(`图片上传失败！原因：${e.message}`);
        throw e;
      }
    },
    isThoughtModifiable() {
      return (
        this.current.thought!.data.status == ThoughtStatus.Unsubmitted ||
        this.current.thought!.data.status == ThoughtStatus.Draft
      );
    },
  },
  watch: {
    "filter.class"() {
      this.fetchVols();
    },
    infoDlg(v, ov) {
      if (!ov && v) {
        saveScroll();
        return;
      }
      if (ov && !v) {
        resumeScroll();
        return;
      }
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
