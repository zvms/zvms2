<template>
  <i class="my-20">Under construction</i>
</template>

<script lang="ts">
import { fApi } from "@/apis";
import { useInfoStore, useLoadingStore } from "@/stores";
import { mapStores } from "pinia";
import UseridInput from "@/components/userid-input.vue";

export default {
  name: "import-time",
  components: {
    UseridInput,
  },
  data() {
    return {};
  },
  methods: {},
  computed: {
    ...mapStores(useInfoStore, useLoadingStore),
  },
};
</script>
