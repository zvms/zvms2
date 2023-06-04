<template>
  <v-form v-model="isFormValid">
    <v-text-field
      v-model.trim="modelValue.name"
      :rules="rules"
      type="text"
      label="义工名称"
      prepend-icon="mdi-pen"
      autocomplete="modelValue.name"
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
      v-model="modelValue.type"
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
      <v-row v-for="(cls, i) in modelValue.classes" :key="cls.id" class="py-0">
        <v-col cols="4" class="pl-16" style="font-size: large">
          {{ classes.find((v) => v.id == cls.id)?.name }}
        </v-col>
        <v-col cols="4" class="pl-7" style="font-size: large">
          {{ cls.max }}
        </v-col>
        <v-col cols="2">
          <v-btn rounded class="mx-2 delete" flat @click="delFromList(i)">
            <v-icon size="x-large"> mdi-minus </v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
    <v-text-field
      v-else
      v-model.number="modelValue.classes[0].max"
      :label="`允许${infoStore.className}报名的人数`"
      type="text"
      prepend-icon="mdi-account-multiple"
    />
    <!---->
    <v-text-field
      v-model.trim="modelValue.time"
      :rules="[TIME(), ...rules]"
      type="text"
      label="预期进行时间（e.g. 23-9-1-10-30表示23年9月1日10时30分）"
      prepend-icon="mdi-calendar-range"
    />
    <v-textarea
      v-model.trim="modelValue.description"
      :rules="rules"
      type="text"
      label="义工描述"
      prepend-icon="mdi-text"
    />
    <v-text-field
      v-model.number="modelValue.reward"
      :rules="[IS_DECIMAL(), IS_POSITIVE(), IS_VAILD(), ...rules]"
      type.trim="text"
      label="预期时长（分钟）"
      prepend-icon="mdi-clock-time-three-outline"
    />

    <v-card-actions>
      <v-btn
        :color="primaryStyle ? 'primary' : ''"
        :class="primaryStyle ? 'submit' : ''"
        @click="submit"
      >
        {{ submitButtonName }}
      </v-btn>
      <v-btn v-if="showCancel" @click="$emit('cancel')"> 取消 </v-btn>
    </v-card-actions>
  </v-form>
</template>

<script lang="ts">
import { type PropType } from "vue";
import { fApi, type SingleClass, VolType, type Volunteer } from "@/apis";
import { IS_DECIMAL, IS_POSITIVE, NOT_EMPTY, TIME, IS_VAILD } from "@/utils/validation";
import { mapStores } from "pinia";
import { useInfoStore } from "@/stores";
import { Categ } from "@/apis/types/enums";
import { toasts, validateForm } from "@/utils/dialogs";

export default {
  name: "vol-editor",
  props: {
    modelValue: {
      type: Object as PropType<Volunteer>,
      required: true,
    },
    showCancel: {
      type: Boolean,
      default: () => false,
    },
    primaryStyle: {
      type: Boolean,
      default: () => false,
    },
    submitButtonName: {
      type: String,
      required: true,
    },
  },
  emits: ["update:modelValue", "submit", "cancel"],
  data() {
    return {
      TIME,
      IS_DECIMAL,
      IS_POSITIVE,
      IS_VAILD,
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
      ] as (SingleClass & { selected: boolean })[],
      rules: [NOT_EMPTY()],
      isFormValid: false,
    };
  },
  beforeMount() {
    if (this.advancedOptionsPermission) {
      fApi.skipOkToast.listClasses()((classes) => {
        this.classes = classes.map((cls) => ({
          ...cls,
          selected:
            this.modelValue.classes.findIndex((v) => v.id === cls.id) !== -1,
        }));
        this.setDefaultClass();
      });
    }
  },
  methods: {
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
        this.modelValue.classes.unshift({
          id: this.classNew,
          max: this.countNew,
        });
        this.classes[idx].selected = true;
        this.setDefaultClass();
      });
    },
    delFromList(i: number) {
      const id = this.modelValue.classes.splice(i, 1)[0].id;
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
    submit() {
      if (validateForm(this.isFormValid)) {
        if (
          this.advancedOptionsPermission &&
          this.modelValue.classes.length === 0
        ) {
          toasts.error("必须至少选择一个班级。请点击“+”号添加班级");
          return;
        }
        this.$emit("submit");
      }
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
  watch: {
    modelValue: {
      handler(newValue: Volunteer) {
        this.$emit("update:modelValue", newValue);
      },
      deep: true,
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
