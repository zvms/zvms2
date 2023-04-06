<template>
  <v-table dense>
    <v-list>
      <v-list-item>
        <v-list-item-title>简介</v-list-item-title>
        <div v-html="vol.name"></div>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>时间</v-list-item-title>
        {{ vol.time }}
      </v-list-item>
      <v-list-item>
        <v-list-item-title>
          {{ getVolTypeName(vol.type) }}（预期）时长
          <span style="font-size: medium"
            >&emsp;&emsp;注：实际获得时长由审计部决定。</span
          >
        </v-list-item-title>
        {{ timeToHint(vol.reward) }}
      </v-list-item>
      <v-list-item>
        <v-list-item-title>创建者</v-list-item-title>
        {{ vol.holderName }}
      </v-list-item>
      <!-- <v-list-item>
        <v-list-item-title>参与者（{{ vol.joiners.length }}人）</v-list-item-title>
        <v-list-item-title v-for="j in vol.joiners">{{ j.name }}</v-list-item-title>
      </v-list-item> -->
      <!-- <v-list-item>
          <v-list-item-title>人数</v-list-item-title>
          {{ vol.maxJoiner }}
        </v-list-item> -->
      <v-list-item>
        <v-list-item-title>
          已报名（{{ vol.joiners.length }}人）
        </v-list-item-title>
        <v-chip label small v-for="j in vol.joiners" class="ma-1">{{
          j.name
        }}</v-chip>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>状态</v-list-item-title>
        {{ getVolStatusNameForUser(infoStore.userId, vol) }}
        <!-- {{ getVolArrangedName(vol.isArranged) }} -->
      </v-list-item>
    </v-list>
  </v-table>
</template>

<script lang="ts">
import { getVolStatusNameForUser, timeToHint } from "@/utils/calc";
import { type VolunteerInfoResponse, getVolTypeName } from "@/apis";
import { type PropType } from "vue";
import { mapStores } from "pinia";
import { useInfoStore } from "@/stores";

export default {
  name: "vol-info",
  props: {
    vol: {
      type: Object as PropType<VolunteerInfoResponse>,
      required: true,
    },
  },
  data() {
    return {
      timeToHint,
      getVolTypeName,
      getVolStatusNameForUser,
    };
  },
  computed: {
    ...mapStores(useInfoStore),
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
