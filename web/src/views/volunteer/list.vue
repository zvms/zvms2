<template>
  <v-container>
    <v-card color="primary" dark>
      <v-card-title>
        义工列表
        <v-spacer></v-spacer>
      </v-card-title>
    </v-card>

    <v-data-table
      fixed-header
      :headers="headers"
      :items="participantsLst"
      :search="search"
      loading-text="加载中..."
      no-data-text="没有数据哦"
      no-results-text="没有结果"
    >
    </v-data-table>

    <v-dialog v-model="dialog1" max-width="80%">
      <v-card>
        <v-table style="margin: 20px">
          <thead>
            <td>学号</td>
            <td>删除</td>
          </thead>
          <tbody>
            <tr v-for="(stuid, i) in stulstSelected" :key="i">
              <td>{{ mp[stuid] }}</td>
              <td>
                <v-btn
                  class="mx-2"
                  fab
                  dark
                  x-small
                  color="primary"
                  @click="delFromList(i)"
                >
                  <v-icon dark> mdi-minus </v-icon>
                </v-btn>
              </td>
            </tr>
            <tr>
              <td>
                <v-select
                  prepend-icon="mdi-switch"
                  v-model="stu_new"
                  label="选定学生"
                  :items="stulst"
                  item-text="name"
                  item-value="id"
                >
                </v-select>
              </td>
              <td>
                <v-btn
                  class="mx-2"
                  fab
                  dark
                  x-small
                  color="primary"
                  @click="addToList"
                >
                  <v-icon dark> mdi-plus </v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
        <p>
          当前选中了{{
            stulstSelected.length
          }}个学生哦，你可以点击加号添加一个学生
        </p>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="signupVolunteer(volid)"
            >确定</v-btn
          >
          <v-btn color="red darken-1" text @click="dialog1 = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialog2" max-width="80%">
      <v-card>
        <v-card-title>感想提交（班级）</v-card-title>

        <div v-if="pictures.length > 0" style="left: 50px; position: relative">
          <v-card-text>图片（点击图片以删除）</v-card-text>
          <ul v-for="(pic, i) in pictures" :key="i">
            <li>
              <img
                :src="'data:image/png;base64,' + pic"
                class="pic"
                @click="removePic(i)"
                style="cursor: pointer"
              />
            </li>
          </ul>
        </div>

        <v-divider></v-divider>

        <v-table style="margin: 20px" v-if="thoughts.length > 0">
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
        </v-table>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="choosePictures()"
            >选择义工图片</v-btn
          >
          <v-btn color="red darken-1" text @click="chooseCSV()"
            >选择义工感想csv</v-btn
          >
          <v-btn color="red darken-1" text @click="submitThought()">提交</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { toasts } from "@/utils/dialogs.js";
import { permissionTypes } from "@/utils/permissions";
import volinfo from "@/components/vol-info.vue";
import { fApi } from "@/apis";
import axios from "axios";
import { useInfoStore } from "@/stores";
import { mapStores } from "pinia";
import { VDataTable } from "vuetify/labs/VDataTable";

export default {
  components:{
    volinfo,
    VDataTable
  },
  data() {
    return {

    }
  },
  mounted() {

  },
  methods: {
  }
  computed: {
    ...mapStores(useInfoStore),
  },
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
