<template>
  <v-list>
    <v-list-item>
      <v-list-item-title>感想 <span v-if="showWordCount" style="font-size: medium;">&emsp;&emsp;中文字数：{{ getWordCount(thought.thought??"") }}</span></v-list-item-title>
      <div v-html="thought.thought"></div>      
    </v-list-item>
    <v-list-item v-if="thought.pics">
      <v-list-item-title>图片</v-list-item-title>
      <v-container>
        <v-row>
          <v-col v-for="(img, i) in thought.pics" :key="i">
            <v-img
              :src="`${baseURL}/static/pics/${img.hash}${img.type}`"
              max-width="10em"
              outlined
              @click="
                showImage = true;
                currentImage = `${baseURL}/static/pics/${img.hash}${img.type}`;
              "
            />
          </v-col>
        </v-row>
      </v-container>
    </v-list-item>
    <v-dialog v-model="showImage" scrollable @click="showImage = false">
      <v-list>
        <v-list-item>
          <v-img :src="currentImage" />
        </v-list-item>
      </v-list>
    </v-dialog>
  </v-list>
</template>

<script lang="ts">
import { timeToHint } from "@/utils/calc";
import {
  getVolTypeName,
  type ThoughtInfoResponse,
} from "@/apis";
import type { PropType } from "vue";
import { baseURL } from "@/plugins/axios";

export default {
  name: "thought-info",
  props: {
    thought: {
      type: Object as PropType<ThoughtInfoResponse>,
      required: true,
    },
    showWordCount: {
      type: Boolean,
      default: ()=>false,
    }
  },
  data() {
    return {
      timeToHint,
      getVolTypeName,
      baseURL,
      showImage: false,
      currentImage: "",
    };
  },
  methods: {
    getWordCount(str: string) {
      let n = 0;
      for (let i = 0; i < str.length; i++) {
        let c = str.charAt(i);
        if (c.match(/[\u4e00-\u9fa5\u9FA6-\u9fcb]/)) {
          n++;
        }
      }
      return n;
    }
  }
};
</script>
<style scoped>
.v-list-item-title {
  padding-top: 10px;
  font-size: larger;
  border-bottom: 1px black solid;
}
</style>
