<template>
  <v-container>
    <v-card>
      <v-card-title> 创建义工 </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field v-model="form.name" :rules="rules" label="义工名称" prepend-icon="mdi-pen" />
          <v-text-field v-model="form.stuMax" :rules="rules" label="义工总人数" prepend-icon="mdi-account" />
          <!---->
          <v-simple-table>
            <thead>
              <td>班级</td>
              <td>最多报名人数</td>
              <td></td>
            </thead>
            <tbody>
              <tr v-for="(cls, i) in classSelected" :key="i">
                <td>{{ mp[cls.id] }}</td>
                <td>{{ cls.stuMax }}</td>
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
                  <v-select prepend-icon="mdi-switch" v-model="class_new" label="限定班级" :items="classes" item-text="name"
                    item-value="id">
                  </v-select>
                </td>
                <td>
                  <v-text-field v-model.number="count_new" label="限制人数">
                  </v-text-field>
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
          <!---->
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
          <v-text-field v-model="form.description" :rules="rules" label="义工描述" prepend-icon="mdi-text" />
          <v-text-field v-model="form.inside" label="校内时长（分钟）" prepend-icon="mdi-view-list" />
          <v-text-field v-model="form.outside" label="校外时长（分钟）" prepend-icon="mdi-view-list" />
          <v-text-field v-model="form.large" label="大型时长（分钟）" prepend-icon="mdi-view-list" />
        </v-form>
        <v-card-actions>
          <v-btn color="primary" block @click="createVolunteer">创建义工</v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>
    <br />
  </v-container>
</template>

<script lang="ts">
import { toasts } from "../../utils/dialogs";
import { fApi, checkToken } from "../../apis";
import { NOTEMPTY } from "../../utils/validation.js";

export default {
  data: () => ({
    classSelected: [],
    count_new: undefined,
    class_new: undefined,
    classes: undefined,
    modalDate: false,
    modalTime: false,
    form: {
      name: undefined,
      date: undefined,
      time: null,
      stuMax: undefined,
      description: undefined,
      inside: undefined,
      outside: undefined,
      large: undefined,
      class: undefined,
    },
    rules: [NOTEMPTY()],
    mp: {}
  }),
  components: {},
  mounted () {
    this.pageload();
  },
  methods: {
    async pageload() {
      await checkToken();
      let classes = await fApi.fetchClassList();
      classes
        ? (this.classes = classes)
        : toasts.error("获取班级列表失败");

      for (const cls of this.classes)
        this.mp[cls.id] = cls.name;
    },
    createVolunteer: async function () {
      if (this.$refs.form.validate()) {
        // if (true){
        console.log("创建义工");
        console.log(this.form);

        // 义工时间默认为0
        if (!this.form.inside && !this.form.outside && !this.form.large) {
          toasts.error("义工时间可不能全为0啊...");
          return;
        }

        this.form.inside = parseInt(this.form.inside) || 0;
        this.form.outside = parseInt(this.form.outside) || 0;
        this.form.large = parseInt(this.form.large) || 0;

        if (this.form.stuMax != parseInt(this.form.stuMax) || isNaN(parseInt(this.form.stuMax)) || parseInt(this.form.stuMax) <= 0 ||
          this.form.inside != parseInt(this.form.inside) || parseInt(this.form.inside) < 0 ||
          this.form.outside != parseInt(this.form.outside) || parseInt(this.form.outside) < 0 ||
          this.form.large != parseInt(this.form.large) || parseInt(this.form.large) < 0) {
          toasts.error("数据不合法");
          return;
        }

        let data = await fApi.createVol(this.form.name,
          this.form.date,
          this.form.time,
          parseInt(this.form.stuMax),
          this.form.description,
          parseInt(this.form.inside),
          parseInt(this.form.outside),
          parseInt(this.form.large),
          this.classSelected,
        )
        toasts.success(data.message);

        const d = new Date();
        this.classSelected.forEach(async (i) => {
          await fApi.sendNotice(
            [i.id],
            `新的义工：${this.form.name}（限报人数：${i.stuMax}）`,
            d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + (d.getDate() + 2),
            this.form.description, () => {
              for (let k in this.form)
                this.form[k] = undefined
              this.classSelected = []
            }
          )
        });

        this.$router.push('/me');
      }
    },
    addToList () {
      let flg = false;
      if (this.class_new == "") flg = true;
      if (isNaN(parseInt(this.count_new)) || parseInt(this.count_new) <= 0) flg = true;
      for (let i in this.classSelected) {
        console.log(i);
        if (this.classSelected[i]["id"] == this.class_new) {
          flg = true;
          break;
        }
      }
      if (!flg)
        this.classSelected.push({ "id": this.class_new, "stuMax": parseInt(this.count_new) });
      this.class_new = "";
      this.count_new = 0;
    },
    delFromList (i) {
      this.classSelected.splice(i, 1);
    }
  }
};
</script>

<style scoped>
.v-card {
  margin: 0.3rem;
}
</style>