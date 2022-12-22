<template>
  <v-container>
    <v-card>
      <v-card-title>初始化</v-card-title>
      <v-card-text>正在加载...</v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import {checkToken} from "../apis";
export default {
  name: "home",
  mounted () {
    this.pageload();
  },
  methods: {
    pageload: async function(){
      await checkToken();
      this.$router.push("/me");
    }
  },
};
</script>
