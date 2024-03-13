<template>
  <v-sheet>
    <v-breadcrumbs :items="breadcrumbs"></v-breadcrumbs>
    <transition
      enter-active-class="animate__animated animate__fadeInDown"
      leave-active-class="animate__animated animate__fadeOutDown"
    >
      <div v-if="!changing">
        <h1 v-if="breadcrumbs.length !== 1 && !changing">
          {{ currentDoc.title }}
        </h1>

        <v-list density="compact">
          <v-list-item
            v-if="currentDoc.parent"
            prepend-icon="mdi-arrow-u-left-top"
            @click="goBack"
          >
            <span class="link-tip">返回</span>
            {{ currentDoc.parent!.title }}
          </v-list-item>
          <v-list-item
            prepend-icon="mdi-file-document-outline"
            v-for="c in currentDoc.children"
            @click="gotoDoc(c.urlPath)"
          >
            {{ c.title }}
          </v-list-item>
        </v-list>

        <article
          v-if="!changing"
          class="markdown-body"
          v-html="currentDoc.content"
        ></article>
      </div>
    </transition>
  </v-sheet>
</template>

<script lang="ts">
import { mapStores } from "pinia";
import { docs, type DocItem } from "@/docs";
import { useDialogStore } from "@/stores";
import "github-markdown-css/github-markdown-light.css";
import { toasts } from "@/plugins/toastification";

export default {
  data() {
    return {
      currentDoc: undefined as any as DocItem,
      changing: false,
    };
  },
  beforeMount() {
    this.load(this.$route.params.docId);
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
      this.$router.push("/");
      return false;
    },
    gotoDoc(path: string) {
      this.changing = true;
      this.$router.push(path);
      setTimeout(() => {
        this.changing = false;
      }, 100);
    },
    goBack() {
      this.changing = true;
      this.$router.push(this.currentDoc.parent!.urlPath);
      setTimeout(() => {
        this.changing = false;
      }, 200);
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
    ...mapStores(useDialogStore),
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
