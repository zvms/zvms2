<template>
  <v-card flat>
    <v-layout column align-center>
      <v-card-title v-if="toggled == false && stu.status == 1"
        ><span class="cert-header">义工完成证明</span></v-card-title
      >
      <v-card-title v-if="toggled == true || stu.status != 1">{{
        vol.name
      }}</v-card-title>
    </v-layout>
    <v-container fluid>
      <div v-if="toggled == false && stu.status == 1" @click="flipcard()">
        <p class="cert">
          <span class="stress">{{ stuname }}</span
          >同学已于<span class="stress">{{ formalTime(vol.time) }}</span
          >完成名为<span class="stress">{{ vol.name }}</span
          >的义工活动，预计获得校内义工时长<span class="stress">{{
            timeToHint(vol.inside)
          }}</span
          >，校外义工时长<span class="stress">{{
            timeToHint(vol.outside)
          }}</span
          >，大型义工时长<span class="stress"
            >{{ timeToHint(vol.large) }}。</span
          >
        </p>
        <p class="cert">
          经由团支部评定及感想审核，决定给予<span class="stress">{{
            stuname
          }}</span
          >同学校内义工时长<span class="stress">{{
            timeToHint(stu.inside)
          }}</span
          >，校外义工时长<span class="stress">{{
            timeToHint(stu.outside)
          }}</span
          >，大型义工时长<span class="stress">{{ timeToHint(stu.large) }}</span
          >。
        </p>
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
              <pre v-for="i in vol.description.split('\n')" v-bind:key="i">{{
                i
              }}</pre>
            </fieldset>
          </v-col>
          <v-divider class="mx-4" vertical></v-divider>
          <v-col style="line-height: 2.5">
            <v-chip color="primary"> {{ formalDate(vol.date) }} </v-chip>
            <v-chip color="primary"> {{ formalTime(vol.time) }} </v-chip>
            <v-chip color="primary"> {{ stu.id }} </v-chip>
            <v-chip color="primary"> {{ stuname }} </v-chip>
            <v-chip
              :color="stColor(stu.status)"
              :text-color="stColorT(stu.status)"
            >
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

<script lang="ts">
import { fApi, VolStatus, type SingleVolunteer } from "../apis";
import { toasts } from "../utils/dialogs";
import { timeToHint } from "@/utils/calc";

export default {
  name: "vol-cert",
  props: ["volid", "stuid", "stuname"],
  data: () => ({
    timeToHint,
    volid: NaN,
    stuid: NaN,
    stuName: "",
    toggled: false,
    vol: undefined as SingleVolunteer,
  }),
  created() {
    this.update();
  },
  methods: {
    stColor(a: VolStatus) {
      if (a == VolStatus.Audited) return "green";
      if (a == VolStatus.Unaudited) return "red";
      return "";
    },
    stColorT(a: VolStatus) {
      if (a == VolStatus.Audited) return "white";
      if (a == VolStatus.Unaudited) return "white";
      return "black";
    },
    flipcard() {
      this.toggled = !this.toggled;
    },
    haveThought() {
      return this.vol.thought.length > 0;
    },
    update() {
      this.toggled = false;
      if (Number.isFinite(this.volid)) {
        let data = await fApi.volcert(this.volid, this.stuid);
        if (data.type == "ERROR") toasts.error(data.message);
        else if (data.type == "SUCCESS") {
          this.vol = data.vol;
          this.stu = data.stu;
        } else toasts.error("未知错误");
      }
    },
  },
  watch: {
    volid() {
      this.update();
    },
    stuid() {
      this.update();
    },
    stuname() {
      this.update();
    },
  },
};
</script>

<style>
fieldset {
  border: 2px solid #92baee;
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
