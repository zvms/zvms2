<template>
  <v-container>
    <v-card color="primary" dark>
      <v-card-title>
        义工列表
        <v-spacer></v-spacer>
      </v-card-title>
    </v-card>
    <v-card v-for="vol in volworks" v-bind:key="vol.id">
      <v-card-title>{{ vol.name }}</v-card-title>
      <v-card-text>
        {{ vol.description }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="volDetail(vol.id)">
          <v-icon left>mdi-clipboard-text</v-icon>
          详情
        </v-btn>
        <v-btn color="primary" @click="participants(vol.id)">
          <v-icon left>mdi-clipboard-text</v-icon>
          查看已报名
        </v-btn>
        <v-btn v-if="granted()" color="primary" @click="thoughtSubmitDialog(vol.id)">
          <v-icon left>mdi-upload</v-icon>
          感想提交
        </v-btn>
        <v-btn v-if="granted()" color="primary" @click="volSignUp(vol.id)">
          <v-icon left>mdi-account-plus</v-icon>
          报名
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-dialog v-model="dialog" max-width="80%">
      <v-card>
        <volinfo :volid="volid" />
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="dialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialog_participant" max-width="80%">
      <v-card>
        <v-card-title>报名列表</v-card-title>
        <v-card-text>
          <v-data-table fixed-header :headers="headers" :items="participantsLst" :search="search" loading-text="加载中..."
            no-data-text="没有数据哦" no-results-text="没有结果">
          </v-data-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="dialog_participant = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialog1" max-width="80%">
      <v-card>
        <v-simple-table style="margin:20px;">
          <thead>
            <td>学号</td>
            <td>删除</td>
          </thead>
          <tbody>
            <tr v-for="(stuid, i) in stulstSelected" :key="i">
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
                <v-select prepend-icon="mdi-switch" v-model="stu_new" label="选定学生" :items="stulst" item-text="name"
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
        <p>当前选中了{{ stulstSelected.length }}个学生哦，你可以点击加号添加一个学生</p>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="signupVolunteer(volid)">确定</v-btn>
          <v-btn color="red darken-1" text @click="dialog1 = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialog2" max-width="80%">
      <v-card>
        <v-card-title>感想提交（班级）</v-card-title>

        <div v-if="pictures.length > 0" style="left: 50px; position: relative;">
          <v-card-text>图片（点击图片以删除）</v-card-text>
          <ul v-for="(pic, i) in pictures" :key="i">
            <li>
              <img :src="'data:image/png;base64,' + pic" class="pic" @click="removePic(i)" style="cursor: pointer">
            </li>
          </ul>
        </div>

        <v-divider></v-divider>

        <v-simple-table style="margin:20px;" v-if="thoughts.length > 0">
          <thead>
            <td>学号</td>
            <td>感想</td>
          </thead>
          <tbody>
            <tr v-for="(thought, i) in thoughts" :key="i">
              <td>{{ thought.stuId }}</td>
              <td>{{ thought.thought }}</td>
            </tr>
          </tbody>
        </v-simple-table>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="choosePictures()">选择义工图片</v-btn>
          <v-btn color="red darken-1" text @click="chooseCSV()">选择义工感想csv</v-btn>
          <v-btn color="red darken-1" text @click="submitThought()">提交</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { toasts } from "@/utils/dialogs.js";
import { permissionTypes } from "@/utils/permissions";
import volinfo from "@/components/volinfo.vue";
import { fApi, checkToken } from "@/apis";
import axios from "axios";
import { useInfoStore, useLastseenvolStore } from "@/stores";
import { mapStores } from "pinia";

interface Volwork{
  id:number
}

export default {
  data: () => ({
    search: "",
    headers: [
      { text: "学号", value: "stuId", align: "start", sortable: true },
      { text: "姓名", value: "stuName" },
    ],
    volworks: [] as Volwork[],
    dialog: false,
    dialog_participant: false,
    dialog1: false,

    dialog2: false,
    curVolId: null,
    pictures: [],
    thoughts: [],

    submitThoughtDialog: false,
    volid: undefined,
    onlyDisplayCurrentClass: true,
    stulst: undefined,
    stulstSelected: [],
    stu_new: undefined,
    participantsLst: [],
    stu: undefined,
    thought: undefined,
    mp: {}
  }),
  components: {
    volinfo,
  },
  mounted () {
    this.pageload();
  },
  methods: {
    async pageload() {
      await checkToken();
      let volworks:Volwork[] = await this.fetchVol();
      this.volworks = volworks.sort((a, b) => b.id - a.id);
      this.lastseenvolStore.lastseenvol = this.volworks;
    },
    granted () {
      return this.infoStore.permission < permissionTypes.teacher;
    },
    async volSignUp(volid) {
      console.log("SignUp: " + volid);
      this.dialog1 = true;

      this.stulst = undefined;
      this.stulstSelected = [];
      let stulst = await fApi.fetchStudentList(this.infoStore.class);
      stulst
        ? (this.stulst = stulst)
        : toasts.error("获取学生列表失败");
      this.volid = volid;
      for (const i in this.stulst)
        this.mp[this.stulst[i].id] = this.stulst[i].name;
    },
    thoughtSubmitDialog (volId) {
      this.dialog2 = true;
      this.curVolId = volId;
    },
    removePic(i) {
      this.pictures.splice(i, 1)
    },
    choosePictures: async function () {
      await fApi.openPictures((data) => {
        if (data === null) return;

        this.pictures.push(data)
      })
    },
    chooseCSV: async function () {
      await fApi.openCSV((data) => {
        if (data === null) return;

        this.thoughts = []

        data = data.split('\n')
        data.shift()

        let error = false;
        data.forEach(e => {
          if (error) return

          let v = e.split(',')
          if (v.length < 2) {
            if (!(v.length == 1 && v[0] == "")) {
              toasts.error(`${e}格式有问题`)
              error = true
            }
            return
          }

          v = [v[0]].concat(v.slice(1).join(','))

          if (isNaN(parseInt(v[0]))) {
            toasts.error(`学号${v[0]}不合法（必须是纯数字）`)
            error = true
            return
          }
          this.thoughts.push({
            stuId: v[0],
            thought: v[1]
          })
        });

        console.log(this.thoughts)

      })
    },
    submitThought() {
      this.dialog2 = false;

      this.thoughts.forEach((e) => {
        console.log(parseInt(e.stuId), e.stuId)
        axios
          .post("/volunteer/thought/" + this.curVolId, {
            "thought": [{
              "stuId": parseInt(e.stuId),
              "content": e.thought,
              "pictures": this.pictures
            }],
          })
          .then((response) => {
            // console.log(response.data);
            if (response.data.type == "SUCCESS") {
              toasts.success(response.data.message);
              // location.reload();
              this.pageload()
            } else {
              toasts.error(response.data.message);
            }
          })
          .catch((err) => {
            toasts.error(err);
          })
          .finally(() => {

          });
      })
      this.pictures = []
      this.thoughts = []
      this.curVolId = null

    },
    signupVolunteer (volid) {
      if (this.stulstSelected.length == 0) {
        toasts.error("报名列表为空");
        return;
      }
      axios
        .post("/volunteer/signup/" + volid, {
          "stulst": this.stulstSelected
        })
        .then((response) => {
          // console.log(response.data);
          if (response.data.type == "SUCCESS") {
            toasts.success(response.data.message);
            for (let k in this.form)
              this.form[k] = undefined
          } else {
            toasts.error(response.data.message);
          }
        })
        .catch((err) => {
          toasts.error(err);
        })
        .finally(() => {

        });
      this.dialog1 = false;
    },

    participants: async function (volid) {
      this.dialog_participant = true;
      this.volid = volid;
      this.participantsLst = await fApi.fetchSignerList(volid);
    },

    volDetail(volid) {
      this.volid = volid;
      this.dialog = true;
    },

    async fetchVol() {
      if (this.granted()) return await this.fetchCurrentClassVol();
      else return await this.fetchAllVol();
    },
    async fetchCurrentClassVol() {
      let volworks = await fApi.fetchClassVolunter(this.infoStore.class);
      if (!volworks) toasts.error("获取义工列表失败");
      return volworks;
    },
    async fetchAllVol() {
      let volworks = await fApi.fetchAllVolunter();
      if (!volworks) toasts.error("获取义工列表失败");
      return volworks;
    },

    addToList () {
      // console.log("Ent");
      // console.log(this.stu_new);
      // console.log(this.stulstSelected);
      let flg = false;
      if (this.stu_new == undefined) flg = true;
      for (let i in this.stulstSelected) {
        if (this.stulstSelected[i] == this.stu_new) {
          flg = true;
          break;
        }
      }
      if (!flg)
        this.stulstSelected.push(this.stu_new);
      else
        toasts.error("请不要重复报名");
      this.stu_new = undefined;
    },
    delFromList (i) {
      this.stulstSelected.splice(i, 1);
    }
  },
  computed: {
    ...mapStores(useLastseenvolStore, useInfoStore)
  }
};
</script>

<style scoped>
.v-card {
  margin: 0.3rem;
}

.pic {
  width: auto;
  height: 120px;
}
</style>