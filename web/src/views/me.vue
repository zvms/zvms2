<template>
  <v-card>
    <v-card-title>
      你好,
      <v-card-text>
        {{ infoStore.username }}
        <v-chip v-for="chip in chips" v-bind:key="chip.id" class="ma-2">
          <v-icon left>{{ chip.icon }}</v-icon>
          {{ chip.content }}
        </v-chip>
      </v-card-text>
    </v-card-title>
    <v-card-actions>
      <v-btn @click="modifyPwd">修改密码</v-btn>
      <v-btn @click="logout">登出</v-btn>
    </v-card-actions>
  </v-card>

  <v-card>
    <v-card-title> 通知 </v-card-title>
    <v-list shaped>
      <v-list-item
        color="primary"
        v-for="(notice, i) in noticesStore.notices"
        :key="i"
        @click="showNotice(notice)"
      >
        <v-list-item icon>
          <v-icon>mdi-message</v-icon>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>{{ notice.title }}</v-list-item-title>
          <v-list-item-subtitle>{{ notice.content }}</v-list-item-subtitle>
        </v-list-item>
      </v-list-item>
    </v-list>
  </v-card>

  <v-dialog v-model="dialog" max-width="80%">
    <v-card>
      <v-card-title>{{ curNoticeTitle }}</v-card-title>
      <v-card-text v-html="curNoticeText"></v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { useInfoStore, useNoticesStore } from "@/stores";
import { fApi, type NoticeBody } from "@/apis";
import { permissionNames, permissionTypes } from "@/utils/permissions";
import { mapStores } from "pinia";
import router from "@/router";
import { applyNavItems } from "@/utils/nav";

export default {
  name: "me",
  data() {
    return {
      chips: [] as { id: number; icon: string; content: string }[],
      dialog: false,
      curNoticeTitle: "",
      curNoticeText: "",
      timer: "",
    };
  },
  mounted() {
    if (!(this.infoStore.permission & permissionTypes.logined)) {
      console.log("login!");
      router.push("/login");
    }
    this.chips = [
      ...(Number.isFinite(this.infoStore.classId)
        ? [{ id: -1, icon: "mdi-label", content: this.infoStore.className }]
        : []),
      ...Object.keys(permissionNames).map((key, i) => {
        return {
          id: i,
          icon: "mdi-label",
          content: (permissionNames as any)[key as any],
        };
      }),
    ];
  },
  methods: {
    showNotice(notice: NoticeBody) {
      this.curNoticeTitle = notice.title;
      let s = "";
      for (const c of notice.content) {
        if (c == "\n") {
          s += "<br />";
        } else {
          s += c;
        }
      }
      this.curNoticeText = s;
      this.dialog = true;
    },
    logout() {
      fApi.logout()(() => {
        useInfoStore().$reset();
        applyNavItems();
        router.push("/login");
      });
    },
    modifyPwd() {
      router.push("/modifyPwd");
    },
  },
  computed: {
    ...mapStores(useInfoStore, useNoticesStore),
  },
};
</script>
