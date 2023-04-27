<template>
  <v-card>
    <v-card-title> 您在义工 {{ vol.name }} 的感想 </v-card-title>
    <v-card-text>
      感想状态：
      <br />
      <strong style="font-size: larger">
        {{ getThoughtStatusName(thought.status) }}
      </strong>
      <span v-if="thought.status === ThoughtStatus.Accepted">
        时长{{ thought.reward }}分钟
      </span>
      <span v-if="thought.everRepulsed&&thought.status == ThoughtStatus.Draft" style="color:red">
        （上次提交被打回，请修改感想后重新提交
        <span v-if="thought.reason">
          ，打回原因：
          {{ thought.reason }}
        </span>
        ）
      </span>
      <div class="my-3"></div>
      <v-form>
        感想文字：
        <markdown-editor v-if="isThoughtModifiable" v-model="thought.thought" />
        <markdown-viewer v-else :markdown="thought.thought" label="感想文字" />
        <div class="my-3 divider"></div>
        感想图片：
        <v-tabs v-if="isThoughtModifiable" v-model="tab">
          <v-tab value="from-image-bed"> 通过图片ID上传 </v-tab>
          <v-tab value="from-upload"> 从本地上传（学海平板无效） </v-tab>
        </v-tabs>
        <v-window v-if="isThoughtModifiable" v-model="tab">
          <v-window-item value="from-image-bed">
            <v-text-field label="图片ID" v-model.trim="picsId" />
            <v-btn @click="uploadFromId" style="border: 1px gray solid">
              上传
            </v-btn>
          </v-window-item>
          <v-window-item value="from-upload">
            <v-file-input
              accept="image/*"
              @update:model-value="uploadImg"
              label="感想图片，支持拖入"
            />
          </v-window-item>
        </v-window>

        <v-container>
          <v-row>
            <v-col v-for="(p, i) in pics" :key="p.key">
              <v-img
                :src="p.byHash ? p.url : `data:${p.type};base64,${p.base64}`"
                max-width="10em"
                outlined
              />
              <v-btn
                v-if="isThoughtModifiable"
                color="white"
                @click="pics.splice(i, 1)"
              >
                删除
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn v-if="isThoughtModifiable" @click="submitThought">提交</v-btn>
      <v-btn @click="maySaveThoughtAndClose"
        >{{ isThoughtModifiable ? "保存并" : "" }}关闭</v-btn
      >
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import {
  ThoughtStatus,
  fApi,
  getThoughtStatusName,
  getVolTypeName,
  type Picture,
  type ThoughtInfoResponse,
  type VolunteerInfoResponse,
} from "@/apis";
import MarkdownViewer from "@/components/markdown/viewer.vue";
import MarkdownEditor from "@/components/markdown/editor.vue";
import { baseURL } from "@/plugins/axios";
import { useInfoStore } from "@/stores";
import { timeToHint } from "@/utils/calc";
import { toasts, confirm } from "@/utils/dialogs";
import { ArrayBufferToWordArray, getPicsById } from "@/utils/pics";
import { mapStores } from "pinia";
import type { PropType } from "vue";
import CryptoJS from "crypto-js";

export default {
  name: "thought-editor",
  components: {
    MarkdownViewer,
    MarkdownEditor,
  },
  props: {
    stuName: {
      type: String,
      required: true,
    },
    volId: {
      type: Number,
      required: true,
    },
    vol: {
      type: Object as PropType<VolunteerInfoResponse>,
      required: true,
    },
    stuId: {
      type: Number,
      required: true,
    },
    thought: {
      type: Object as PropType<ThoughtInfoResponse>,
      required: true,
    },
  },
  emits: ["close"],
  data() {
    return {
      timeToHint,
      getVolTypeName,
      getThoughtStatusName,
      ThoughtStatus,
      currentImage: "",
      pics: [] as (
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
      )[],
      picsId: "",
      tab: "from-image-bed",
    };
  },
  created() {
    this.pics = this.thought.pics.map((v) => ({
      byHash: true,
      hash: v.hash,
      type: v.type,
      url: `${baseURL}/static/pics/${v.hash}.${v.type}`,
      key: v.hash,
    }));
  },
  methods: {
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
            this.volId,
            this.infoStore.userId,
            pic
          )((result) => {
            this.pics.push({
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
      this.pics.push({
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
        this.volId,
        this.stuId,
        this.thought.thought ?? "",
        await this.picsForUpload
      )(then);
    },
    async submitThought() {
      if (await confirm("确定提交？提交后不可修改！")) {
        fApi.submitThought(
          this.volId,
          this.infoStore.userId,
          this.thought.thought ?? "",
          await this.picsForUpload
        )(() => {
          this.$emit("close");
        });
      }
    },
    async maySaveThoughtAndClose() {
      if (this.isThoughtModifiable) {
        this.saveThought(() => {
          this.$emit("close");
        });
      } else {
        this.$emit("close");
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    isJoiner() {
      return (
        this.vol.joiners.findIndex((v) => v.id === this.infoStore.userId) !== -1
      );
    },
    async picsForUpload() {
      try {
        const pics: Picture[] = [];
        for (const v of this.pics) {
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
      return this.thought.status == ThoughtStatus.Draft;
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
