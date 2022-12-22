<template>
  <v-container>
    <v-card>
      <v-card-title>义工自提交</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field v-model="form.name" :rules="rules" label="义工名称" prepend-icon="mdi-pen" />

          <v-dialog ref="dateDialog" v-model="modalDate" :return-value.sync="form.date" persistent width="290px">
            <template v-slot:activator="{ on, attrs }">
              <v-text-field v-model="form.date" label="义工日期" :rules="rules" prepend-icon="mdi-calendar" readonly
                v-bind="attrs" v-on="on"></v-text-field>
            </template>
            <v-date-picker v-model="form.date" scrollable>
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="modalDate = false">
                取消
              </v-btn>
              <v-btn text color="primary" @click="$refs.dateDialog.save(form.date)">
                确认
              </v-btn>
            </v-date-picker>
          </v-dialog>
          <v-dialog ref="timeDialog" v-model="modalTime" :return-value.sync="form.time" persistent width="290px">
            <template v-slot:activator="{ on, attrs }">
              <v-text-field v-model="form.time" label="义工时间" prepend-icon="mdi-clock-time-four-outline" readonly
                :rules="rules" v-bind="attrs" v-on="on"></v-text-field>
            </template>
            <v-time-picker v-if="modalTime" v-model="form.time" full-width>
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="modalTime = false">
                取消
              </v-btn>
              <v-btn text color="primary" @click="$refs.timeDialog.save(form.time)">
                确定
              </v-btn>
            </v-time-picker>
          </v-dialog>

          <v-simple-table>
            <thead>
              <td>学号</td>
              <td>删除</td>
            </thead>
            <tbody>
              <tr v-for="(stuid, i) in form.stuSelected" :key="i">
                <td>{{ mp[stuid] }}</td>
                <td>
                  <v-btn class="mx-2" fab dark x-small color="primary" @click="delFromList(i)">
                    <v-icon dark>
                      mdi-minus
                    </v-icon>
                  </v-btn>
                </td>
              </tr>
              <tr>
                <td>
                  <v-select prepend-icon="mdi-switch" v-model="stuNew" label="选定学生" :items="stulst" item-text="name"
                    item-value="id">
                  </v-select>
                </td>
                <td>
                  <v-btn class="mx-2" fab dark x-small color="primary" @click="addToList">
                    <v-icon dark>
                      mdi-plus
                    </v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-simple-table>

          <v-text-field v-model="form.description" :rules="rules" label="义工描述" prepend-icon="mdi-pen" />

          <v-text-field v-model="form.inside" :rules="rules" label="校内义工时长（分钟）" prepend-icon="mdi-pen" />

          <v-text-field v-model="form.outside" :rules="rules" label="校外义工时长（分钟）" prepend-icon="mdi-pen" />

          <v-text-field v-model="form.large" :rules="rules" label="大型活动义工时长（分钟）" prepend-icon="mdi-pen" />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text color="primary" @click="submit">
          提交
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { toasts } from "@/utils/dialogs.js";
import { fApi, checkToken } from "@/apis";
import { NOTEMPTY } from "@/utils/validation.js";
import { useInfoStore } from "@/stores";
import { mapStores } from "pinia";

export default {
  data: () => ({
    modalDate: false,
    modalTime: false,
    stulst: [],
    stuNew: undefined,
    mp: {},
    form: {
      name: undefined,
      date: undefined,
      time: null,
      stuSelected: [],
      description: undefined,
      inside: undefined,
      outside: undefined,
      large: undefined
    },
    rules: [NOTEMPTY()]
  }),
  mounted () {
    this.pageload();
  },
  methods: {
    async pageload() {
      await checkToken();
      let stulst = await fApi.fetchStudentList(this.infoStore.class);
      stulst
        ? (this.stulst = stulst)
        : toasts.error("获取学生列表失败");
      for (let i = 0; i < this.stulst.length; i++)
        this.mp[this.stulst[i].id] = this.stulst[i].name;
    },
    addToList () {
      let flg = false;
      if (this.stuNew == "" || this.stuNew == undefined) flg = true;
      for (let i in this.form.stuSelected) {
        if (this.form.stuSelected[i] == this.stuNew) {
          flg = true;
          break;
        }
      }
      // console.log(this.stuSelected,this.stuNew);
      if (!flg)
        this.form.stuSelected.push(this.stuNew);
      else
        toasts.error("请不要重复报名");
      this.stuNew = "";
    },
    delFromList (i) {
      this.form.stuSelected.splice(i, 1);
    },
    async submit() {
      if (this.form.stuSelected.length == 0) {
        toasts.error("报名学生列表为空");
        return;
      }
      fApi.submitHolidayVol(
           this.form.name,
          this.form.date,
          this.form.time,
          this.form.stuSelected,
          "自提交义工：" + this.form.description,
          isNaN(parseInt(this.form.inside)) ? 0 : parseInt(this.form.inside),
          isNaN(parseInt(this.form.outside)) ? 0 : parseInt(this.form.outside),
          isNaN(parseInt(this.form.large)) ? 0 : parseInt(this.form.large),

      )
    }
  },
  computed:{
    ...mapStores(useInfoStore)
  }
};
</script>

<style scoped>
.v-card {
  margin: 0.3rem;
}
</style>