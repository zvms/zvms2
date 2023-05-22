<template>
  <v-table dense>
    <v-list>
      <v-list-item>
        <v-list-item-title>名称</v-list-item-title>
        <div>{{ vol.name }}</div>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>简介</v-list-item-title>
        <div>{{ vol.description }}</div>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>进行时间</v-list-item-title>
        {{ vol.time }}
      </v-list-item>
      <v-list-item>
        <v-list-item-title>
          {{ getVolTypeName(vol.type) }}（预期）时长
          <span style="font-size: medium">&emsp;&emsp;注：实际获得时长由审计部决定。</span>
        </v-list-item-title>
        {{ timeToHint(vol.reward) }}
      </v-list-item>
      <v-list-item>
        <v-list-item-title>创建者</v-list-item-title>
        <v-chip class="ma-1" label small @click="showStuInfo(vol.holder)">
          {{ vol.holderName }}
        </v-chip>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>报名情况</v-list-item-title>
        <p v-if="volClassesNormalized.length > 0" v-for="c in volClassesNormalized">
          {{ c.name }}：最多可报名{{ c.max }}人
        </p>
        <p v-else>是已经确定成员的义工，无需报名</p>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>
          已报名（{{ vol.joiners.length }}人）
        </v-list-item-title>
        <v-chip label small :closable="false/*(infoStore.permission & (Categ.Manager | Categ.System)) > 0*/"
          v-for="j in vol.joiners" class="ma-1" @click="showStuInfo(j.id)" @click:close="rollbackSignup(j.id)">
          {{ j.name }}
        </v-chip>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>状态</v-list-item-title>
        <v-chip class="ma-1" label :color="getVolStatusDisplayForUser(infoStore.userId, vol)[1]">
          {{ getVolStatusDisplayForUser(infoStore.userId, vol)[0] }}
        </v-chip>
        <!-- {{ getVolArrangedName(vol.isArranged) }} -->
      </v-list-item>
    </v-list>
    <v-dialog v-model="stuInfoDlg">
      <v-card>
        <v-card-title> 用户信息 </v-card-title>
        <v-card-text>
          <StuInfo :student="stuInfoData" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-table>
</template>

<script lang="ts">
import { getVolStatusDisplayText, timeToHint } from "@/utils/calc";
import {
  fApi,
  type VolunteerInfoResponse,
  getVolTypeName,
  type UserInfoResponse,
  Categ
} from "@/apis";
import { type PropType } from "vue";
import { mapStores } from "pinia";
import { useInfoStore } from "@/stores";
import StuInfo from "../stu-info.vue";
import { confirm } from "@/utils/dialogs";

export default {
  name: "vol-info",
  components: {
    StuInfo,
  },
  props: {
    volId: {
      type: Number,
      required: true,
    },
    vol: {
      type: Object as PropType<VolunteerInfoResponse>,
      required: true,
    },
    signupRollupable: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      timeToHint,
      getVolTypeName,
      getVolStatusDisplayForUser: getVolStatusDisplayText,
      Categ,
      stuInfoDlg: false,
      stuInfoData: undefined as any as UserInfoResponse,
    };
  },
  methods: {
    showStuInfo(id: number) {
      fApi.skipOkToast.getUserInfo(id)((info) => {
        this.stuInfoData = info;
        this.stuInfoDlg = true;
      });
    },
    async rollbackSignup(id: number) {
      if (await confirm("确定要撤销报名吗？")) {
        fApi.rollbackSignup(this.volId, id)();
      }
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    volClassesNormalized() {
      return this.vol.classes.filter((v) => v.max > 0);
    },
  },
};
</script>

<style scoped>
.v-list-item-title {
  padding-top: 10px;
  font-size: larger;
  border-bottom: 1px rgb(var(--v-theme-color7)) solid;
  border-radius: 3px;
}
</style>
