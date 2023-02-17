<template>
  <v-card flat>
    <v-card-title>
      {{ vol.name }}
    </v-card-title>
    <v-simple-table dense>
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
          <td>人数</td>
          <td>{{ vol.stuMax }}</td>
        </tr>
        <tr>
          <td>已报名</td>
          <td>{{ vol.stuNow }}</td>
        </tr>
        <tr>
          <td>状态</td>
          <td>{{ getVolStatusName(vol.status )}}</td>
        </tr>
      </tbody>
    </v-simple-table>
  </v-card>
</template>

<script lang="ts">
import { fApi, type VolunteerInfoResponse, getVolTypeName,getVolStatusName } from "../apis";
export default {
  name: "vol-info",
  props: ["volid"],
  data() {
    return {
      volid: NaN,
      getVolTypeName,
      getVolStatusName,
      vol: undefined as VolunteerInfoResponse,
    };
  },
  methods: {
    updateVol() {
      if (Number.isFinite(this.volid)) {
        fApi.getVolunteerInfo(this.volid)((vol) => {
          this.vol = vol;
        });
      }
    },
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
