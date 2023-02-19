<template>
  <v-card flat>
    <v-card-title>
      {{ vol.name }}
    </v-card-title>
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
          <td>
            {{ getVolTypeName(vol.type) }}时长
          </td>
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
  </v-card>
</template>

<script lang="ts">
import { fApi, type VolunteerInfoResponse, getVolTypeName } from "../apis";
import { timeToHint } from "@/utils/calc";

export default {
  name: "vol-info",
  props: ["volid"],
  data() {
    return {
      getVolTypeName,
      volid: NaN,
      vol: 1 as VolunteerInfoResponse,
    };
  },
  methods: {
    async updateVol() {
      if (Number.isFinite(this.volid)) {
        fApi.getVolunteerInfo(this.volid)((vol) => {
          this.vol = vol;
        });
      }
    },
    timeToHint,
  },
  watch: {
    volid: {
      immediate: true,
      handler() {
        this.updateVol();
      },
    },
  },
};
</script>
