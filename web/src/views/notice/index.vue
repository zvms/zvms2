<template>
    <v-card>
      <v-card-title> 创建通知 </v-card-title>
      <v-card-text>
        <v-tabs v-model="tab">
          <v-tab v-for="t in tabs" :value="t.id"> {{ t.name }} </v-tab>
        </v-tabs>
        <v-window v-model="tab" style="font-size: larger">
          <v-window-item v-for="t in tabs" :value="t.id">
            <component :is="t.component" />
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </template>
  
  <script lang="ts">
  import CreateSchool from "./create-school.vue";
  import CreateUser from "./create-user.vue";
  
  export default {
    name: "notice",
    data() {
      return {
        tab: "create-school",
      };
    },
    computed: {
      tabs() {
        return [
          {
            name: "创建全校通知",
            id: "create-school",
            component: CreateSchool,
          },
          {
            name: "创建个人通知",
            id: "create-user",
            component: CreateUser,
          },
        ];
      },
    },
  };
  </script>
  