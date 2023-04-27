<template>
  <v-container>
    <v-card>
      <v-card-title>
        我的感想
        <v-btn @click="fetchThoughts" size="xsmall">
          <v-icon icon="mdi-reload" size="xsmall" />
        </v-btn>
      </v-card-title>
      <v-container>
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
    <!-- <v-dialog v-model="thoughtDlg" persistent fullscreen>
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
            <span v-if="current.thought!.data.everRepulsed">
              （上次提交被打回，请修改感想后重新提交
              <span v-if="current.thought!.data.reason">
                ，打回原因：
                {{ current.thought!.data.reason }}
              </span>
              ）
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
      </v-dialog> -->
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
