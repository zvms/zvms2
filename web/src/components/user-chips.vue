<template>
  <v-chip label v-for="chip in chips" :key="chip.id" class="ma-2">
    <v-icon left>{{ chip.icon }}</v-icon>
    {{ chip.content }}
  </v-chip>
</template>

<script lang="ts">
import { getCategName } from "@/apis";

export default {
  name: "user-chips",
  props: {
    className: {
      type: String,
      required: true,
    },
    permission: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {};
  },
  computed: {
    chips(): { id: number; icon: string; content: string }[] {
      return [
        {
          id: 0,
          icon: "mdi-account-multiple",
          content: this.className,
        },
        ...[2, 4, 8, 16, 32, 64, 128]
          .filter((id) => id & this.permission)
          .map((id) => ({
            id,
            icon: "mdi-check-decagram",
            content: getCategName(id),
          })),
      ];
    },
  },
};
</script>
