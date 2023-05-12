<template>
  <userid-input v-model="newStuId" />
</template>
<script lang="ts">
import UseridInput from "../userid-input.vue";
export default {
  name: "signup-editor",
  components: {
    UseridInput,
  },
  props: {
    volId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      newStuId: "",
      signups: [] as string[],
    };
  },
  methods: {
    addSignup() {
        this.signups.push(this.newStuId);
        this.newStuId = "";
    },
  },
  computed: {},
};
</script>
