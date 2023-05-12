<template>
  <v-list density="compact">
    <v-list-item v-for="s in signups">
      {{ s.name }}
    </v-list-item>
  </v-list>
</template>
<script lang="ts">
import type { SingleUserWithoutAuth } from "@/apis";
import type { PropType } from "vue";
export default {
  name: "signup-viewer",
  components: {},
  props: {
    signups: {
      type: Object as PropType<SingleUserWithoutAuth[]>,
      required: true,
    },
  },
  data() {},
  methods: {},
  computed: {},
};
</script>
