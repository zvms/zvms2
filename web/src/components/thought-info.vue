<template>
  <v-table dense>
    <tbody>
      <tr>
        <td>感想</td>
        <td>{{ thought.thought }}</td>
      </tr>
      <tr v-if="thought.pics">
        <td>图片</td>
        <td>
          <ul v-for="img in thought.pics" :key="img">
            <li>
              <img :src="'data:image/png;base64,' + img" class="pic" />
            </li>
          </ul>
        </td>
      </tr>
    </tbody>
  </v-table>
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
