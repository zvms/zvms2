<template>
  <v-list>
    <v-list-item>
      <v-list-item-title>感想</v-list-item-title>
      {{ thought.thought }}
    </v-list-item>
    <v-list-item v-if="thought.pics">
      <v-list-item-title>图片</v-list-item-title>

      <ul v-for="img in thought.pics" :key="img">
        <li>
          <img :src="'data:image;base64,' + img" class="pic" />
        </li>
      </ul>
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
