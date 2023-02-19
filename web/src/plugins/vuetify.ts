import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { md1 } from "vuetify/blueprints";
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default createVuetify({
  components,
  directives,
  blueprint: md1,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    }
  },
});
