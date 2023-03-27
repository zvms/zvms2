<template>
  <v-container>
    <v-card>
      <v-card-title> 创建义工 </v-card-title>
      <v-card-text>
        <v-form v-model="isFormValid">
          <v-text-field
            v-model="form.name"
            :rules="rules"
            type="text"
            label="义工名称"
            prepend-icon="mdi-pen"
          />
          <!---->
          <v-container v-if="selectClassPermission">
            <v-row v-if="unselctedClasses.length > 0">
              <v-col cols="3">
                <v-select
                  prepend-icon="mdi-account-group"
                  v-model="classNew"
                  label="限定班级"
                  :items="unselctedClasses"
                  item-title="name"
                  item-value="id"
                />
              </v-col>
              <v-col cols="3">
                <v-text-field
                  v-model.number="countNew"
                  type="text"
                  label="限制人数"
                />
              </v-col>
              <v-col cols="2">
                <v-btn rounded class="mx-2 add" flat @click="addToList">
                  <v-icon size="x-large"> mdi-plus </v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-row v-for="(cls, i) in form.classSelected" :key="cls.id">
              <v-col cols="3" class="pl-16">
                {{ classes.find((v) => v.id == cls.id)?.name }}
              </v-col>
              <v-col cols="3" class="pl-7">{{ cls.max }}</v-col>
              <v-col cols="2">
                <v-btn rounded class="mx-2 delete" flat @click="delFromList(i)">
                  <v-icon size="x-large"> mdi-minus </v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
          <v-text-field
            v-else
            v-model.number="countNew"
            label="限制人数"
            type="number"
            prepend-icon="mdi-account-group"
          />
          <!---->
          <v-text-field
            v-model="form.date"
            :rules="rules"
            type="text"
            label="日期（e.g. 23-9-1）"
            prepend-icon="mdi-calendar-range"
          />
          <v-textarea
            v-model="form.description"
            :rules="rules"
            type="text"
            label="义工描述"
            prepend-icon="mdi-text"
          />
          <v-text-field
            v-model.number="form.reward"
            :rules="rules"
            type="text"
            label="预期时长（分钟）"
            prepend-icon="mdi-clock-time-three-outline"
          />
          <v-btn color="primary" type="submit" @click="createVolunteer"
            >创建义工</v-btn
          >
        </v-form>
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
import { Categ } from "@/apis/types/enums";
import { toasts } from "@/utils/dialogs";

export default {
  data() {
    return {
      Categ,
      countNew: "" as any as number,
      classNew: NaN,
      classes: [] as (SingleClass & { selcted?: boolean })[],
      form: {
        name: "",
        date: "",
        description: "",
        reward: "" as any as number,
        classSelected: [] as ClassVol[],
        type: VolType.Outside,
        class: undefined,
      },
      rules: [NOTEMPTY()],
      isFormValid: false,
    };
  },
  mounted() {
    fApi.skipOkToast.listClasses()((classes) => {
      this.classes = classes;
      this.setDefaultClass();
    });
  },
  methods: {
    createVolunteer() {
      if (this.isFormValid) {
        if (
          this.selectClassPermission &&
          this.form.classSelected.length === 0
        ) {
          toasts.error("必须至少选择一个班级！");
          return;
        }
        fApi.createVolunteer(
          this.selectClassPermission
            ? this.form.classSelected
            : [
                {
                  id: this.infoStore.classId,
                  max: this.countNew,
                },
              ],
          this.form.name,
          this.form.description,
          this.form.date,
          this.form.type,
          this.form.reward
        )((result) => {
          this.$router.push("/");
        });
      }
    },
    addToList() {
      if(!Number.isFinite(this.countNew)){
        return;
      }
      const idx = this.classes.findIndex((v) => v.id == this.classNew);
      this.form.classSelected.unshift({
        id: this.classNew,
        max: this.countNew,
      });
      this.classes[idx].selcted = true;
      this.setDefaultClass();
    },
    delFromList(i: number) {
      const id = this.form.classSelected.splice(i, 1)[0].id;
      const idx = this.classes.findIndex((v) => v.id == id);
      this.classes[idx].selcted = false;
      this.setDefaultClass();
    },
    setDefaultClass() {
      const myClass = this.infoStore.classId;
      if (this.unselctedClasses.findIndex((v) => v.id == myClass) !== -1) {
        this.classNew = myClass;
      } else {
        this.classNew = this.unselctedClasses[0].id;
      }
      this.countNew = "" as any as number;
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    unselctedClasses() {
      return this.classes.filter((v) => !v.selcted);
    },
    selectClassPermission() {
      return (
        this.infoStore.permission &
        (Categ.System | Categ.Manager | Categ.Auditor)
      );
    },
  },
};
</script>
<style scoped>
.v-btn.add,.v-btn.delete{
  border: 2px solid rgb(var(--v-theme-color8));
  margin-left: -90px !important;
}
.v-btn.add{
  margin-top: 10px;
}
.v-btn.delete{
  margin-top: -7px;
}
</style>