<template>
  <p class="disable-click markdown-viewer" v-html="renderedHTML"></p>
</template>

<script lang="ts">
import { sanitize } from "@/utils/sanitize";
import { marked } from "marked";

export default {
  name: "markdown-viewer",
  props: {
    markdown: {
      type: String,
      required: true,
    },
  },
  computed: {
    renderedHTML() {
      return sanitize(marked(this.markdown));
    },
  },
};
</script>
<style scoped>
.markdown-viewer {
  border: 1px grey solid;
  border-radius: 3px;
  padding: 20px;
  font-size: smaller;
}
</style>