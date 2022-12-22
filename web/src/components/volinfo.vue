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
          <td>日期</td>
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
    timeToHint (a) {
      let hr = parseInt(a / 60);
      let mi = parseInt(a % 60);
      if (hr != 0)
        if (mi != 0)
          return hr + " 小时 " + mi + " 分钟";
        else
          return hr + " 小时 ";
      else
        return mi + "分钟";
    },
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
  },
  watch: {
    volid () {
      this.fetch();
    },
  },
};
</script>
