<template>
  <p>{{ student.name }} （{{ student.school_id }}）</p>
  <user-chips :permission="student.auth" :className="student.clsName" />
</template>

<script lang="ts">
import type { PropType } from "vue";
import type { UserInfoResponse } from "@/apis";
import PermissionChips from "./user-chips.vue";

export default {
  name: "stu-info",
  components: { PermissionChips },
  props: {
    student: {
      type: Object as PropType<UserInfoResponse>,
      required: true,
    },
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
