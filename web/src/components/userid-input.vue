<template>
  <div style="height: 20px">
    {{ currentUserInfo }}
  </div>
  <v-text-field
    type="text"
    autocomplete="userid"
    v-model.trim="userId"
    label="ID/学号 &nbsp;&nbsp; e.g. 20221145"
    prepend-icon="mdi-account"
    @update:model-value="updateCurrentUserInfo"
    :rules="rules"
  >
  </v-text-field>
</template>

<script lang="ts">
import { fApiNotLoading } from "@/apis/fApi";
import { NOT_EMPTY } from "@/utils/validation";

export default {
  name: "userid-input",
  props: {
    modelValue: {
      type: String,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      userId: "",
      currentUserInfo: "",
      rules: [NOT_EMPTY()],
    };
  },
  methods: {
    updateCurrentUserInfo() {
      this.$emit("update:modelValue", this.userId);
      const userId = parseInt(this.userId);
      if (!Number.isFinite(userId) || ("" + userId).length !== 8) {
        this.currentUserInfo = "";
        return;
      }
      fApiNotLoading.skipOkToast.getUserBasicInfo(userId)(
        ({ clsName, userName }) => {
          this.currentUserInfo = `${clsName} ${userName}`;
        }
      );
    },
  },

  watch: {
    modelValue(newVal) {
      this.userId = newVal;
      this.updateCurrentUserInfo();
    },
  },
};
</script>
