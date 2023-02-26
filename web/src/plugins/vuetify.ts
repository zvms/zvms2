import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { md1 } from "vuetify/blueprints";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "@mdi/font/css/materialdesignicons.css";
import { VDataTable } from "vuetify/labs/VDataTable";

export default createVuetify({
  components: {
    ...components,
    //VDataTable
  },
  directives,
  blueprint: md1,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
});
