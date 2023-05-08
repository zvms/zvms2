<template>
  <article
    class="markdown-body markdown-viewer"
    v-html="renderedHtml"
  ></article>
</template>

<script lang="ts">
import { sanitize } from "@/utils/sanitize";
import { marked } from "marked";
import "github-markdown-css";

export default {
  name: "markdown-viewer",
  props: {
    markdown: {
      type: String,
      required: true,
    },
  },
  computed: {
    renderedHtml() {
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
