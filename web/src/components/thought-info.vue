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
  fApi,
  type VolunteerInfoResponse,
  getVolTypeName,
  getVolStatusName,
  type ThoughtInfoResponse,
} from "@/apis";
export default {
  name: "thought-info",
  props: ["thought"],
  data() {
    return {
      timeToHint,
      getVolTypeName,
      getVolStatusName,
      thought: undefined as ThoughtInfoResponse,
    };
  },
};
</script>
