<template>
  <v-list>
    <v-list-item>
      <v-list-item-title>感想</v-list-item-title>
      {{ thought.thought }}
    </v-list-item>
    <v-list-item v-if="thought.pics">
      <v-list-item-title>图片</v-list-item-title>
      <v-container>
        <v-row>
          <v-col v-for="(img, i) in thought.pics" :key="i">
            <v-img
              :src="`data:${img.type};base64,${img.base64}`"
              max-width="10em"
              outlined
            />
          </v-col>
        </v-row>
      </v-container>
    </v-list-item>
  </v-list>
</template>

<script lang="ts">
import { timeToHint } from "@/utils/calc";
import {
  getVolTypeName,
  getVolStatusName,
  type ThoughtInfoResponse,
} from "@/apis";
import type { PropType } from "vue";

export default {
  name: "thought-info",
  props: {
    thought: {
      type: Object as PropType<ThoughtInfoResponse>,
      required: true,
    },
  },
  data() {
    return {
      timeToHint,
      getVolTypeName,
      getVolStatusName,
    };
  },
};
</script>
<style scoped>
.v-list-item-title {
  padding-top: 10px;
  font-size: larger;
  border-bottom: 1px black solid;
}
</style>
