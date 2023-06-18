<template>
  <MdEditor
    :modelValue="modelValue"
    @update:modelValue="updateModelValue"
    :toolbars="toolbars"
    :sanitize="sanitize"
    previewTheme="github"
  />
</template>

<script lang="ts">
import { sanitize } from "@/utils/sanitize";

import MdEditor, { type ToolbarNames } from "md-editor-v3";
import "md-editor-v3/lib/style.css";

export default {
  name: "markdown-editor",
  components: {
    MdEditor,
  },
  props: {
    modelValue: {
      type: String,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      sanitize,
    };
  },
  methods: {
    updateModelValue(payload: string) {
      this.$emit("update:modelValue", payload);
    },
  },
  computed: {
    toolbars() {
      return [
        "italic",
        "underline",
        "bold",
        "-",
        "title",
        "quote",
        "unorderedList",
        "orderedList",
        "-",
        "prettier",
      ] as ToolbarNames[];
    },
  },
};
</script>
