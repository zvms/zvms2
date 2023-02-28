<template>
  <v-table dense>
    <tbody>
      <tr>
        <td>简介</td>
        <td>{{ vol.description }}</td>
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
        <td>主持</td>
        <td>{{ vol.holderName }}</td>
      </tr>
      <tr v-if="vol.isArranged">
        <td>参与者（{{ vol.joiners.length }}人）</td>
        <td v-for="j in vol.joiners">{{ j.name }}</td>
      </tr>
      <div v-else>
        <tr>
          <td>人数</td>
          <td>{{ vol.maxJoiner }}</td>
        </tr>
        <tr>
          <td>已报名（{{ vol.joiners.length }}人）</td>
          <td v-for="j in vol.joiners">{{ j.name }}</td>
        </tr>
      </div>
      <tr>
        <td>状态</td>
        <td>{{ getVolStatusName(vol.status) }}</td>
        <td>{{ getVolArrangedName(vol.isArranged) }}</td>
      </tr>
    </tbody>
  </v-table>
</template>

<script lang="ts">
import { timeToHint } from "@/utils/calc";
import {
  type VolunteerInfoResponse,
  getVolTypeName,
  getVolStatusName,
} from "@/apis";
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
      getVolStatusName,
    };
  },
};
</script>
