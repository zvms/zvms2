<template>
  <v-card flat>
    <v-layout column align-center>
      <v-card-title v-if="toggled == false && stu.status == 1"><span class="cert-header">义工完成证明</span></v-card-title>
      <v-card-title v-if="toggled == true || stu.status != 1">{{ vol.name }}</v-card-title>
    </v-layout>
    <v-container fluid>
      <div v-if="toggled == false && stu.status == 1" @click="flipcard()">
        <p class="cert"><span class="stress">{{ stuname }}</span>同学已于<span class="stress">{{ formalDate(vol.date) }}
            {{ formalTime(vol.time) }}</span>完成名为<span class="stress">{{ vol.name }}</span>的义工活动，预计获得校内义工时长<span
            class="stress">{{ timeToHint(vol.inside) }}</span>，校外义工时长<span class="stress">{{ timeToHint(vol.outside)
            }}</span>，大型义工时长<span class="stress">{{ timeToHint(vol.large) }}。</span></p>
        <p class="cert">经由团支部评定及感想审核，决定给予<span class="stress">{{ stuname }}</span>同学校内义工时长<span class="stress">{{
            timeToHint(stu.inside)
        }}</span>，校外义工时长<span class="stress">{{ timeToHint(stu.outside) }}</span>，大型义工时长<span class="stress">{{
    timeToHint(stu.large)
}}</span>。</p>
        <p class="cert">特此证明</p>
        <v-layout column align-end>
          <p class="cert">镇海中学 团委</p>
          <p class="cert">镇海中学 学生会实践部</p>
          <p class="cert">镇海中学 义管会</p>
          <p class="cert">{{ formalDate(vol.date) }}</p>
          <v-img src="../../public/stamp.png" height="150px" width="150px" />
        </v-layout>
      </div>
      <div v-if="toggled == true || stu.status != 1" @click="flipcard()">
        <v-row>
          <v-col :cols="8">
            <fieldset>
              <legend>义工描述</legend>
              <pre v-for="i in vol.description.split('\n')" v-bind:key="i">{{ i }}</pre>
            </fieldset>
          </v-col>
          <v-divider class="mx-4" vertical></v-divider>
          <v-col style="line-height:2.5;">
            <v-chip color="primary"> {{ formalDate(vol.date) }} </v-chip>
            <v-chip color="primary"> {{ formalTime(vol.time) }} </v-chip>
            <v-chip color="primary"> {{ stu.id }} </v-chip>
            <v-chip color="primary"> {{ stuname }} </v-chip>
            <v-chip :color="stColor(stu.status)" :text-color="stColorT(stu.status)">
              {{ statusToStr(stu.status) }}
            </v-chip>
          </v-col>
        </v-row>
        <fieldset v-if="haveThought()">
          <legend>学生感想</legend>
          <pre v-for="i in stu.thought.split('\n')" v-bind:key="i">{{ i }}</pre>
        </fieldset>
      </div>
    </v-container>
  </v-card>
</template>
  
<style>
fieldset {
  border: 2px solid #92BAEE;
  border-radius: 10px;
}

legend {
  margin: 0 0 0 30px;
}

pre {
  margin: 15px;
  white-space: pre-wrap;
  white-space: -moz-pre-wrap;
  white-space: -o-pre-wrap;
  word-break: normal;
  word-wrap: break-word;
  font-family: "微软雅黑";
  text-indent: 2em;
}

.stress {
  font-size: 25px;
  font-family: "楷体";
  font-weight: normal;
}

.cert-header {
  font-size: 30px;
  font-family: "宋体";
  font-weight: bold;
}

p.cert {
  text-indent: 2em;
  line-height: 2;
  font-size: 18px;
  font-family: "仿宋";
}
</style>
  
<script lang="ts">
import { fApi } from "../apis";
import { toasts } from "../utils/dialogs";

export default {
  name: "volcert",
  props: ["volid", "stuid", "stuname"],
  data: () => ({
    toggled: false,
    vol: {
      id: undefined,
      name: "加载中...",
      date: undefined,
      time: undefined,
      description: undefined,
      inside: undefined,
      outside: undefined,
      large: undefined,
    },
    stu: {
      id: undefined,
      status: undefined,
      thought: "",
      inside: undefined,
      outside: undefined,
      large: undefined,
    },
  }),
  created () {
    this.init();
  },
  methods: {
    statusToStr (a) {
      if (a == 1) return "通过";
      if (a == 2) return "打回，不可重新提交";
      if (a == 3) return "打回，可以重新提交";
      return "等待审核";
    },
    stColor (a) {
      if (a == 1) return "green";
      if (a == 2) return "red";
      if (a == 3) return "orange";
      return "";
    },
    stColorT (a) {
      if (a == 1) return "white";
      if (a == 2) return "white";
      if (a == 3) return "white";
      return "black";
    },
    formalDate (date) {
      let y = date.slice(0, 4);
      let m = date.slice(5, 7);
      let d = date.slice(8, 10);
      return parseInt(y) + "年" + parseInt(m) + "月" + parseInt(d) + "日";
    },
    formalTime (time) {
      let hr = time.slice(0, 2);
      let mn = time.slice(3, 5);
      return parseInt(hr) + "时" + parseInt(mn) + "分";
    },
    flipcard () {
      this.toggled = !this.toggled;
    },
    haveThought () {
      return this.stu.thought.length > 0;
    },
    init: async function () {
      this.toggled = false;
      if (this.volid != 0 && this.volid != undefined
        && this.stuid != 0 && this.stuid != undefined) {

        let data = await fApi.volcert(this.volid, this.stuid);
        if (data.type == "ERROR")
          toasts.error(data.message);
        else if (data.type == "SUCCESS") {
          this.vol = data.vol;
          this.stu = data.stu;
        } else toasts.error("未知错误");
      }
    },
  },
  watch: {
    volid () { this.init(); },
    stuid () { this.init(); },
    stuname () { this.init(); },
  },
};
</script>
  