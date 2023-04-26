<template>
  <v-sheet>
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <article class="markdown-body" v-html="currentDoc.content"></article>

    <v-list class="pl-10">
      <v-list-item
        v-if="currentDoc.parent"
        prepend-icon="mdi-file-document-outline"
        @click="goBack"
      >
        <span class="link-tip">返回</span> {{ currentDoc.parent!.title }}
      </v-list-item>
      <v-list-item
        prepend-icon="mdi-file-document-outline"
        v-for="c in currentDoc.children"
        @click="gotoDoc(c.urlPath)"
      >
        <span class="link-tip">继续阅读</span> {{ c.title }}
      </v-list-item>
    </v-list>
  </v-sheet>
</template>

<script lang="ts">
import { docs, type DocItem } from "@/docs";
import { toasts } from "@/utils/dialogs";
import "github-markdown-css";
import mermaid from "mermaid";

export default {
  data() {
    return {
      currentDoc: undefined as any as DocItem,
    };
  },
  beforeMount() {
    this.load(this.$route.params.docId);
  },
  mounted() {
    this.renderMermaid();
  },
  updated() {
    this.renderMermaid();
  },
  methods: {
    load(docId: string | string[]): boolean {
      if (
        typeof docId === "string" &&
        docs[docId as keyof typeof docs] !== undefined
      ) {
        this.currentDoc = docs[docId as keyof typeof docs];
        return true;
      }
      toasts.error(`找不到文档 "${docId}"`);
      return false;
    },
    renderMermaid() {
      mermaid.run({
        querySelector: ".language-mermaid",
      });
    },
    gotoDoc(path: string) {
      this.$router.push(path);
    },
    goBack() {
      this.$router.push(this.currentDoc.parent!.urlPath);
    },
  },
  beforeRouteUpdate(to, _from, next) {
    if (this.load(to.params.docId)) {
      next();
    } else {
      next("/docs");
    }
  },
  computed: {
    breadcrumbs() {
      return this.currentDoc.path
        .map((p) => ({
          title: docs[p].title,
          disabled: false,
          to: docs[p].urlPath,
        }))
        .concat({
          title: this.currentDoc.title,
          disabled: true,
          to: "<NULL>",
        });
    },
  },
};
</script>

<style scoped>
.link-tip {
  color: #555;
  font-size: smaller;
}
</style>
