<template>
  <v-container>
    <v-card>
      <v-card-title>
        你好,
        <v-card-text>
          {{ infoStore.username }}
          <v-chip v-for="chip in chips" v-bind:key="chip.id">
            <v-icon left>{{ chip.icon }}</v-icon>
            {{ chip.content }}
          </v-chip>
        </v-card-text>
      </v-card-title>
    </v-card>
    <!-- <v-card dark color="primary">
      <v-card-title>
        <v-icon left>mdi-message</v-icon>
        <span class="font-weight-light title">随机感想</span>
      </v-card-title>
      <v-card-text class="headline font-weight-bold"
        >"{{ thought.content }}"</v-card-text
      >
      <v-card-actions>
        <v-list-item class="grow">
          <v-list-item-avatar>
            <v-icon class="elevation-6">mdi-account-circle</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ thought.stuName }}</v-list-item-title>
          </v-list-item-content>
          <v-tooltip left max-width="300">
            <template v-slot:activator="{ on, attrs }">
              <v-icon class="mr-1" v-bind="attrs" v-on="on"
                >mdi-help-circle</v-icon
              >
            </template>
            <span>这是在所有感想中随机提取的一条。</span>
          </v-tooltip>
        </v-list-item>
      </v-card-actions>
    </v-card> -->

    <v-card>
      <v-card-title>
        通知
      </v-card-title>
      <v-list shaped>
        <v-list-item-group color="primary">
          <v-list-item
            v-for="(notice, i) in $store.state.notices"
            :key="i"
            @click="showNotice(notice)"
          >
            <v-list-item-icon>
              <v-icon>mdi-message</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ notice.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ notice.text }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>
    
    <v-dialog v-model="dialog" max-width="80%">
      <v-card>
        <v-card-title>{{ curNoticeTitle }}</v-card-title>
        <v-card-text v-html="curNoticeText"></v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { useInfoStore } from "@/stores";
import { VContainer, VCard, VCardTitle, VCardText, VChip, VIcon, VList, VListItem, VListItemTitle, VListItemSubtitle, VDialog } from "vuetify/lib/components";
import {fApi, checkToken} from "../apis";
import {permissionNames} from "../utils/permissions";

export default {
  name: "me",
  data: () => ({
    chips: [] as any[],
    thought: {
      stuName: undefined,
      stuId: undefined,
      content: undefined,
    },
    notices: [],
    dialog: false,
    curNoticeTitle: "",
    curNoticeText: "",
    timer: undefined
  }),
  mounted () {
    this.initChips();
    // this.randomThought();
  },
  methods: {
    pageload: async function () {
      await checkToken();
    },
    initChips () {
      this.chips = [
        {
          id: 1,
          icon: "mdi-label",
          content: permissionNames[this.infoStore.permission],
        },
        { id: 2, icon: "mdi-label", content: this.infoStore.classname },
        { id: 3, icon: "mdi-label", content: this.infoStore.class },
      ];
    },
    randomThought: async function () {
      this.thought  = await fApi.fetchRandomThought();
    },
    showNotice(notice) {
      this.dialog = true;
      this.curNoticeTitle = notice.title;
      let s = "";
      for (const c of notice.text) {
        if (c == "\n") {
          s += "<br />"
        } else {
          s += c
        }
      }
      this.curNoticeText = s;
    }
  },
  
};
</script>

<style scoped>
.v-card {
  margin: 1rem;
}

.v-chip {
  margin: 2px;
}
</style>