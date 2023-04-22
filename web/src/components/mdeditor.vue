<template>
  <MdEditor v-model="modelValue" :toolbars="toolbars" :sanitize="sanitize" />
</template>

<script lang="ts">
import type { IOptions } from "sanitize-html";
import sanitizeHtml from "sanitize-html";

import MdEditor, { type ToolbarNames } from "md-editor-v3";
import "md-editor-v3/lib/style.css";

export default {
  name: "zvms-mdeditor",
  components: {
    MdEditor,
  },
  props: {
    modelValue: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
    };
  },
  methods: {
    sanitize(dirtyContent: string) {
      const rule: IOptions = {
        allowedTags: [
          "address",
          "article",
          "aside",
          "footer",
          "header",
          "h1",
          "h2",
          "h3",
          "h4",
          "h5",
          "h6",
          "hgroup",
          "main",
          "nav",
          "section",
          "blockquote",
          "dd",
          "div",
          "dl",
          "dt",
          "figcaption",
          "figure",
          "hr",
          "li",
          "main",
          "ol",
          "p",
          "pre",
          "ul",
          "abbr",
          "b",
          "bdi",
          "bdo",
          "br",
          "cite",
          "code",
          "data",
          "dfn",
          "em",
          "i",
          "kbd",
          "mark",
          "q",
          "rb",
          "rp",
          "rt",
          "rtc",
          "ruby",
          "s",
          "samp",
          "small",
          "span",
          "strong",
          "sub",
          "sup",
          "time",
          "u",
          "var",
          "wbr",
          "caption",
          "col",
          "colgroup",
          "table",
          "tbody",
          "td",
          "tfoot",
          "th",
          "thead",
          "tr",
        ],
        disallowedTagsMode: "discard",
        selfClosing: [
          "br",
          "hr",
          "area",
          "base",
          "basefont",
          "input",
          "link",
          "meta",
        ],
      };
      const cleanHTML = sanitizeHtml(dirtyContent, rule);
      return cleanHTML;
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
