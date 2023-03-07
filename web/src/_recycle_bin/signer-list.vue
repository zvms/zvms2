<template>
  <v-table dense>
    <tbody>
      <tr>
        <td>学号</td>
        <td>{{ vol.holder }}</td>
      </tr>
      <tr>
        <td>姓名</td>
        <td>{{ vol.holderName }}</td>
      </tr>
      <tr>
        <td>时间</td>
        <td>{{ vol.time }}</td>
      </tr>
      <tr>
        <td>{{ getVolTypeName(vol.type) }}时长</td>
        <td>{{ timeToHint(vol.reward) }}</td>
      </tr>
      <tr>
        <td>最多人数</td>
        <td>{{ vol.joiners.length }}人</td>
      </tr>
      <tr>
        <td>已报名人数</td>
        <td>{{ vol }}</td>
      </tr>
      <tr>
        <td>状态</td>
        <td>{{ vol. }}</td>
      </tr>
    </tbody>
  </v-table>
</template>

<script lang="ts">
import { type VolunteerInfoResponse, getVolTypeName } from "../apis";
import { timeToHint } from "@/utils/calc";
import type { PropType } from "vue";

export default {
  name: "vol-info",
  props: {
    timeToHint,
    vol: {
      type: Object as PropType<VolunteerInfoResponse>,
      required: true,
    },
  },
  data() {
    return {
      getVolTypeName,
    };
  },
};
</script>
