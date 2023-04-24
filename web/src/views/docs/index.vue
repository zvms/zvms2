<template>
  <v-sheet>
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <h1>{{ currentDoc.title }}</h1>
    <div v-html="currentDoc.content"></div>
    <a v-for="c in currentDoc.children">{{ c.title }}</a>
  </v-sheet>
</template>

<script lang="ts">
import { docs, type DocItem } from "@/docs";
import router from "@/router";
import { toasts } from "@/utils/dialogs";

export default {
  data() {
    return {
      currentDoc: undefined as any as DocItem,
    };
  },
  beforeMount() {
    console.log(docs);
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
  computed: {
    breadcrumbs() {
      return this.currentDoc.path
        .map((p) => ({
          title: docs[p].title,
          disabled: false,
          href: `/docs/${docs[p].path.join("/")}/${doc[p].name}`,
        }))
        .concat({
          title: this.currentDoc.title,
          disabled: true,
          href:"<NULL>"
        });
    },
  },
};
</script>
