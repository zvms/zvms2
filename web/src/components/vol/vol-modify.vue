<template>
  <v-card>
    <v-card-title>
      修改{{ advancedOptionsPermission ? "" : "校外" }}义工
    </v-card-title>
    <v-card-text>
      <v-form v-model="isFormValid">
        <v-text-field
          v-model.trim="form.name"
          :rules="rules"
          type="text"
          label="义工名称"
          prepend-icon="mdi-pen"
          autocomplete="form.name"
        />
        <v-select
          prepend-icon="mdi-shape"
          label="义工类型"
          v-if="advancedOptionsPermission"
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
        <v-container
          v-if="advancedOptionsPermission"
          style="margin-left: -15px"
          class="pt-0 pb-7"
        >
          <v-row style="margin-bottom: -40px">
            <v-col cols="4">
              <v-select
                prepend-icon="mdi-account-multiple"
                v-model="classNew"
                label="限定班级"
                :items="unselectedClasses"
                item-title="name"
                item-value="id"
              />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model.number="countNew"
                type="text"
                label="限制人数"
              />
            </v-col>
            <v-col cols="2">
              <v-btn
                rounded
                class="mx-2 add"
                flat
                @click="addToList"
                :disabled="!(countNew > 0)"
              >
                <v-icon size="x-large"> mdi-plus </v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row
            v-for="(cls, i) in form.classSelected"
            :key="cls.id"
            class="py-0"
          >
            <v-col cols="4" class="pl-16" style="font-size: larger">
              {{ classes.find((v) => v.id == cls.id)?.name }}
            </v-col>
            <v-col cols="4" class="pl-7" style="font-size: larger">{{
              cls.max
            }}</v-col>
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
          :label="`允许${infoStore.className}报名的人数`"
          type="text"
          prepend-icon="mdi-account-multiple"
        />
        <!---->
        <v-text-field
          v-model.trim="form.time"
          :rules="[TIME(), ...rules]"
          type="text"
          label="预期进行时间（e.g. 23-9-1-10-30表示23年9月1日10时30分）"
          prepend-icon="mdi-calendar-range"
        />
        <v-textarea
          v-model.trim="form.description"
          :rules="rules"
          type="text"
          label="义工描述"
          prepend-icon="mdi-text"
        />
        <v-text-field
          v-model.number="form.reward"
          :rules="[IS_DECIMAL(), IS_POSITIVE(), ...rules]"
          type.trim="text"
          label="预期时长（分钟）"
          prepend-icon="mdi-clock-time-three-outline"
        />
        <v-btn color="primary" class="submit" @click="createVolunteer">
          创建义工
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { fApi, type ClassVol, type SingleClass, VolType } from "@/apis";
import { IS_DECIMAL, IS_POSITIVE, NOT_EMPTY, TIME } from "@/utils/validation";
import { mapStores } from "pinia";
import { useInfoStore } from "@/stores";
import { Categ } from "@/apis/types/enums";
import { toasts, validateForm } from "@/utils/dialogs";
import { timeToHint } from "@/utils/calc";

export default {
  data() {
    return {
      TIME,
      IS_DECIMAL,
      IS_POSITIVE,
      VolType,
      Categ,
      countNew: "" as any as number,
      classNew: -1,
      classes: [
        {
          id: -1,
          name: "加载中",
          selected: false,
        } as any,
      ] as (SingleClass & { selected?: boolean })[],
      form: {
        name: "",
        time: "",
        description: "",
        reward: "" as any as number,
        classSelected: [] as ClassVol[],
        type: VolType.Outside,
      },
      rules: [NOT_EMPTY()],
      isFormValid: false,
      volId: "" as any as number,
    };
  },
  beforeMount() {
    if (this.advancedOptionsPermission) {
      fApi.skipOkToast.listClasses()((classes) => {
        this.classes = classes;
        this.setDefaultClass();
      });
    }
    fApi.skipOkToast.getVolunteerInfo(this.volId)((item) => {
      this.form.name = item.name;
      this.form.time = item.time;
      this.form.description = item.description;
      this.form.reward = item.reward;
      this.form.classSelected = item.classes;
      this.form.type = item.type;
    });
  },
  methods: {
    createVolunteer() {
      if (validateForm(this.isFormValid)) {
        if (
          this.advancedOptionsPermission &&
          this.form.classSelected.length === 0
        ) {
          toasts.error("必须至少选择一个班级。请点击“+”号添加班级");
          return;
        }
        if (this.form.reward == 114514 || this.form.reward == 1919810) {
          toasts.error("请不要恶意填写时间！");
          return;
        } else if (this.form.reward > 300) {
          toasts.error(`义工时间过长。有${timeToHint(this.form.reward)}。`);
          return;
        } else if (this.form.reward <= 0) {
          toasts.error("义工时间小于等于0。");
          return;
        } else if (this.form.reward <= 5) {
          toasts.error("义工时间过短，此处的时间单位是分钟。");
          return;
        }
        fApi.createVolunteer(
          this.advancedOptionsPermission
            ? this.form.classSelected
            : [
                {
                  id: this.infoStore.classId,
                  max: this.countNew,
                },
              ],
          this.form.name,
          this.form.description,
          this.form.time,
          this.form.type,
          this.form.reward
        )((_result) => {
          this.$router.push("/");
        });
      }
    },
    addToList() {
      if (!Number.isFinite(this.countNew)) {
        return;
      }
      fApi.skipOkToast.getClassStudentNum(this.classNew)(({ num: maxNum }) => {
        if (this.countNew > maxNum) {
          toasts.error(`超过班级最大人数！最大人数：${maxNum}人。`);
          this.countNew = maxNum;
        }
        const idx = this.classes.findIndex((v) => v.id == this.classNew);
        this.form.classSelected.unshift({
          id: this.classNew,
          max: this.countNew,
        });
        this.classes[idx].selected = true;
        this.setDefaultClass();
      });
    },
    delFromList(i: number) {
      const id = this.form.classSelected.splice(i, 1)[0].id;
      const idx = this.classes.findIndex((v) => v.id == id);
      this.classes[idx].selected = false;
      this.setDefaultClass();
    },
    setDefaultClass() {
      const myClass = this.infoStore.classId;
      if (this.unselectedClasses.findIndex((v) => v.id == myClass) !== -1) {
        this.classNew = myClass;
      } else {
        this.classNew = this.unselectedClasses[0].id;
      }
      this.countNew = "" as any as number;
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    unselectedClasses() {
      return this.classes.filter((v) => !v.selected);
    },
    advancedOptionsPermission() {
      return (
        this.infoStore.permission &
        (Categ.System | Categ.Manager | Categ.Auditor)
      );
    },
  },
};
</script>
<style scoped>
.v-btn.add,
.v-btn.delete {
  color: #777;
  border: 2px solid currentColor;
  margin-left: -90px !important;
  height: 30px;
}

.v-btn.add {
  margin-top: 15px;
}

.v-btn.delete {
  margin-top: -7px;
}
</style>
