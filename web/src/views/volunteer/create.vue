<template>
  <v-card>
    <v-card-title>
      创建{{ advancedOptionsPermission ? "" : "校外" }}义工
    </v-card-title>
    <v-card-text>
      <vol-editor
        v-model="vol"
        primary-style
        @submit="createVol"
        submit-button-name="创建义工"
      />
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { fApi, type ClassVol, VolType, type Volunteer } from "@/apis";
import { mapStores } from "pinia";
import { useInfoStore } from "@/stores";
import { Categ } from "@/apis/types/enums";
import VolEditor from "@/components/vol/editor.vue";

export default {
  components: {
    VolEditor,
  },
  data() {
    return {
      vol: {
        classes: [
          {
            id: NaN,
            max: "" as any,
          },
        ] as ClassVol[],
        name: "",
        description: "",
        time: "",
        type: VolType.Outside,
        reward: 0,
      } as Volunteer,
    };
  },
  created() {
    this.vol.classes[0].id = this.infoStore.classId;
  },
  methods: {
    createVol() {
      fApi.createVolunteer(
        this.vol.classes,
        this.vol.name,
        this.vol.description,
        this.vol.time,
        this.vol.type,
        this.vol.reward
      )(() => {
        this.$router.push("/");
      });
    },
  },
  computed: {
    ...mapStores(useInfoStore),
    advancedOptionsPermission() {
      return (
        this.infoStore.permission &
        (Categ.System | Categ.Manager | Categ.Auditor)
      );
    },
  },
};
</script>
