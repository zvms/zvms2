<template>
  <v-container>
    <v-card>
      <v-card-title> 创建义工 </v-card-title>
      <v-card-text>
        <v-form v-model="isFormValid">
          <v-text-field
            v-model="form.name"
            :rules="rules"
            label="义工名称"
            prepend-icon="mdi-pen"
          />
          <!---->
          <v-table v-if="infoStore.permission & permissionTypes.system">
            <!-- <thead>
              <td>班级</td>
              <td>最多报名人数</td>
              <td></td>
            </thead> -->
            <tbody>
              <tr v-for="(cls, i) in classSelected" :key="i">
                <td class="pa-0">{{ classes.find((v) => v.id === cls.id)?.name }}</td>
                <td>{{ cls.max }}</td>
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
                <td  class="pa-0">
                  <v-select
                    prepend-icon="mdi-account-group"
                    v-model="class_new"
                    label="限定班级"
                  >
                  </v-select>
                </td>
                <td>
                  <v-text-field v-model.number="count_new" label="限制人数">
                  </v-text-field>
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
          <!---->
          <v-text-field
            v-model="form.date"
            :rules="rules"
            label="日期（e.g. 23-9-1）"
            prepend-icon="mdi-calendar-range"
          />
          <v-textarea
            v-model="form.description"
            :rules="rules"
            label="义工描述"
            prepend-icon="mdi-text"
          />
          <v-text-field
            v-model.number="form.reward"
            label="时长（分钟）"
            prepend-icon="mdi-clock-time-three-outline"
          />
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
import { fApi, type ClassVol, type SingleClass, VolType } from "@/apis";
import { NOTEMPTY } from "@/utils/validation.js";
import { mapStores } from "pinia";
import { useInfoStore } from "@/stores";
import { permissionTypes } from "@/utils/permissions";

export default {
  data() {
    return {
      permissionTypes,
      classSelected: [] as ClassVol[],
      count_new: 5,
      class_new: NaN,
      classes: [{id:123,name:"aaa"},{id:456,name:"bbb"}] as SingleClass[],
      form: {
        name: "",
        date: "",
        description: "",
        reward: 0,
        type: NaN as VolType,
        class: undefined,
      },
      rules: [NOTEMPTY()],
      isFormValid: false,
    };
  },
  mounted() {
    fApi.listClasses()((classes) => {
      this.classes = classes;
    });
  },
  methods: {
    createVolunteer() {
      if (this.isFormValid) {
        fApi.createVolunteer(
          this.classSelected,
          this.form.name,
          this.form.description,
          this.form.date,
          this.form.type,
          this.form.reward,
          this.classSelected
        )((result) => {
          this.$router.push("/");
        });
      }
    },
    addToList() {
      let flg = false;
      if (Number.isNaN(this.class_new)) flg = true;
      if (Number.isNaN(this.count_new) || this.count_new <= 0) flg = true;
      for (let i in this.classSelected) {
        console.log(i);
        if (this.classSelected[i]["id"] == this.class_new) {
          flg = true;
          break;
        }
      }
      if (!flg)
        this.classSelected.push({
          id: this.class_new,
          max: this.count_new,
        });
      this.class_new = NaN;
      this.count_new = 0;
    },
    delFromList(i: number) {
      this.classSelected.splice(i, 1);
    },
  },
  computed: {
    ...mapStores(useInfoStore),
  },
};
</script>

<style scoped>
.v-card {
  margin: 0.3rem;
}
</style>
