<template>
  <p>
  {{ student.name }}
</p>
  <permission-chips :permission="student.auth" :className="student.clsName" />
</template>

<script lang="ts">
import type { PropType } from "vue";
import type { UserInfoResponse } from "@/apis";
import PermissionChips from "./permission-chips.vue";

export default {
  name: "stu-info",
  components: { PermissionChips },
  props: {
    student: {
      type: Object as PropType<UserInfoResponse>,
      required: true,
    },
  },
  data() {
    return {};
  },
};
</script>
<style scoped>
.v-list-item-title {
  padding-top: 10px;
  font-size: larger;
  border-bottom: 1px black solid;
}
</style>
