<template>
  <p class="text-center">
    <span v-if="!loadingStore.isLoading">是空的~</span>
    <span v-else>加载中...</span>
  </p>
</template>

<script lang="ts">
import { useLoadingStore } from "@/stores";
import { mapStores } from "pinia";

export default {
  name: "table-placeholder",
  data() {
    return {};
  },
  computed: {
    ...mapStores(useLoadingStore),
  },
};
</script>
