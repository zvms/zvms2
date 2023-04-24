<template>
  <v-sheet>
    <v-breadcrumbs :items="['Foo', 'Bar', 'Fizz']"></v-breadcrumbs>
    <h1>{{ currentDoc.title }}</h1>
    <div v-html="currentDoc.contentHtml"></div>
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
};
</script>
