<template>
  <v-card flat>
    <v-card-title>
      {{ vol.name }}
    </v-card-title>
    <v-simple-table dense>
      <tbody>
        <tr>
          <td>学号</td>
          <td>{{ vol.stuid }}</td>
        </tr>
        <tr>
          <td>姓名</td>
          <td>{{ vol.date }}</td>
        </tr>
        <tr>
          <td>时间</td>
          <td>{{ vol.time }}</td>
        </tr>
        <tr>
          <td>校内时长</td>
          <td>{{ timeToHint(vol.inside) }}</td>
        </tr>
        <tr>
          <td>校外时长</td>
          <td>{{ timeToHint(vol.outside) }}</td>
        </tr>
        <tr>
          <td>大型时长</td>
          <td>{{ timeToHint(vol.large) }}</td>
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
          <td>{{ vol.status }}</td>
        </tr>
      </tbody>
    </v-simple-table>
  </v-card>
</template>

<script lang="ts">
import { fApi } from "../apis";
import { timeToHint } from "@/utils/calc";

export default {
  name: "volinfo",
  props: ["volid"],
  data: () => ({
    vol: {
      type: undefined,
      message: undefined,
      name: "加载中...",
      date: undefined,
      time: undefined,
      stuMax: undefined,
      stuNow: undefined,
      description: undefined,
      status: undefined,
      inside: undefined,
      outside: undefined,
      large: undefined,
    },
  }),
  created () {
    this.init();
  },
  methods: {
    init: async function () {
      if (this.volid != 0 && this.volid != undefined) {
        this.vol = await fApi.fetchOneVolunteer(this.volid);
      }
    },
    fetch () {
      this.vol = {
        type: undefined,
        message: undefined,
        name: "加载中...",
        date: undefined,
        time: undefined,
        stuMax: undefined,
        stuNow: undefined,
        description: undefined,
        status: undefined,
        inside: undefined,
        outside: undefined,
        large: undefined,
      };
      this.init();
    },
    timeToHint,
  },
  watch: {
    volid () {
      this.fetch();
    },
  }
};
</script>
