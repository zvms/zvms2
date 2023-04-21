<template>
  <v-container>
    <v-card>
      <v-card-title> 记录义工 </v-card-title>
      <v-card-text>
        <v-form v-model="isFormValid">
          <v-text-field
            v-model="form.name"
            :rules="rules"
            type="text"
            label="义工名称"
            prepend-icon="mdi-pen"
          />
          <v-select
            prepend-icon="mdi-shape"
            label="义工类型"
            :items="[
              {
                name: '校外义工',
                value: VolType.Outside,
              },
              {
                name: '校内义工',
                value: VolType.Inside,
              },
            ]"
            item-title="name"
            item-value="value"
            v-model="form.type"
          />
          <v-container class="p-0">
            <v-row>
              <v-col cols="3">
                <v-text-field
                  prepend-icon="mdi-account-group"
                  v-model.number="userNew"
                  label="学生学号"
                  @update:model-value="updateUserName"
                />
              </v-col>
              <v-col cols="3" class="pl-7 pt-8" style="font-size: larger">
                {{ userNewName }}
              </v-col>
              <v-col cols="2">
                <v-btn
                  rounded
                  class="mx-2 add"
                  flat
                  @click="addToList"
                  :disabled="!(userNewName.length > 0)"
                >
                  <v-icon size="x-large"> mdi-plus </v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-row v-for="(user, i) in form.joiners" :key="user.id">
              <v-col cols="3" class="pl-16" style="font-size: larger">
                {{ user.id }}
              </v-col>
              <v-col cols="3" class="pl-7" style="font-size: larger">
                {{ user.name }}</v-col
              >
              <v-col cols="2">
                <v-btn rounded class="mx-2 delete" flat @click="delFromList(i)">
                  <v-icon size="x-large"> mdi-minus </v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
          <!---->
          <v-text-field
            v-model="form.time"
            :rules="[TIME(), ...rules]"
            type="text"
            label="时间（e.g. 23-9-1-10-30表示23年9月1日10时30分）"
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
            label="记录的时长（分钟）"
            prepend-icon="mdi-clock-time-three-outline"
          />
          <v-btn color="primary" class="submit" @click="recordVolunteer">
            记录义工
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <br />
  </v-container>
</template>

<script lang="ts">
import {
  fApi,
  type ClassVol,
  type SingleClass,
  VolType,
  type SingleUserWithoutAuth,
} from "@/apis";
import { NOTEMPTY, TIME } from "@/utils/validation.js";
import { mapStores } from "pinia";
import { useInfoStore } from "@/stores";
import { Categ } from "@/apis/types/enums";
import { toasts } from "@/utils/dialogs";
import { ForegroundApi } from "@/apis/fApi";
import router from "@/router";

export default {
  data() {
    return {
      TIME,
      VolType,
      Categ,
      userNew: "" as any as number,
      userNewName: "",
      form: {
        joiners: [] as SingleUserWithoutAuth[],
        name: "",
        time: "",
        description: "",
        reward: "" as any as number,
        type: VolType.Outside,
      },
      rules: [NOTEMPTY()],
      isFormValid: false,
    };
  },
  methods: {
    recordVolunteer() {
      if (this.isFormValid) {
        fApi.createAppointedVolunteer(
          this.form.joiners.map((v) => v.id),
          this.form.name,
          this.form.description,
          this.form.time,
          this.form.type,
          this.form.reward
        )(() => {
          router.push("/");
        });
      }
    },
    addToList() {
      if (this.form.joiners.findIndex((v) => v.id === this.userNew) === -1) {
        this.form.joiners = [
          { id: this.userNew, name: this.userNewName },
          ...this.form.joiners,
        ];
      }
      this.userNew = "" as any;
      this.userNewName = "";
    },
    delFromList(i: number) {
      this.form.joiners.splice(i, 1);
    },
    updateUserName() {
      if (!Number.isFinite(this.userNew) || ("" + this.userNew).length !== 8) {
        this.userNewName = "";
        return;
      }
      const sepcialFApi = new ForegroundApi({
        beforeReq(info) {},
        errorReq(e: Error, info) {},
        successedRes(res, info) {},
        failedRes: (res, info) => {
          this.userNewName = "";
        },
        afterProcess(info) {},
        errorProcess(e, info) {},
        cleanup(info) {},
        defaultFailedToast: false,
        defaultOkToast: false,
      });
      sepcialFApi.skipOkToast.getUserInfo(this.userNew)((info) => {
        this.userNewName = info.name;
      });
    },
  },
  computed: {
    ...mapStores(useInfoStore),
  },
};
</script>
<style scoped>
.v-btn.add,
.v-btn.delete {
  border: 2px solid rgb(var(--v-theme-color8));
  margin-left: -90px !important;
}
.v-btn.add {
  margin-top: 10px;
}
.v-btn.delete {
  margin-top: -7px;
}
</style>
