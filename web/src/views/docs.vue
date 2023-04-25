<template>
  <v-sheet>
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <article class="markdown-body" v-html="currentDoc.content"></article>

    <v-list class="pl-10">
      <v-list-item
        v-if="hasParent"
        prepend-icon="mdi-file-document-outline"
        @click="goBack"
      >
        返回
      </v-list-item>
      <v-list-item
        prepend-icon="mdi-file-document-outline"
        v-for="c in currentDoc.children"
        @click="gotoDoc(c.urlPath)"
        >{{ c.title }}</v-list-item
      >
    </v-list>
  </v-sheet>
</template>

<script lang="ts">
import { docs, type DocItem } from "@/docs";
import router from "@/router";
import { toasts } from "@/utils/dialogs";
import "github-markdown-css";

export default {
  data() {
    return {
      currentDoc: undefined as any as DocItem,
    };
  },
  beforeMount() {
    this.load();
  },
  methods: {
    load() {
      const docId = this.$route.params.docId;
      if (
        typeof docId === "string" &&
        docs[docId as keyof typeof docs] !== undefined
      ) {
        this.currentDoc = docs[docId as keyof typeof docs];
        return;
      }
      toasts.error(`找不到文档 ${docId}`);
      router.back();
    },
    gotoDoc(path: string) {
      this.$router.push(path);
      this.load();
    },
    goBack() {
      this.$router.back();
      this.load();
    },
  },
  computed: {
    breadcrumbs() {
      return this.currentDoc.path
        .map((p) => ({
          title: docs[p].title,
          disabled: false,
          href: docs[p].urlPath,
        }))
        .concat({
          title: this.currentDoc.title,
          disabled: true,
          href: "<NULL>",
        });
    },
    hasParent() {
      return this.currentDoc.path.length > 0;
    },
  },
};
</script>
