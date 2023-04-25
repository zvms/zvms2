import "vuetify/styles";
import { createVuetify } from "vuetify";
import { pl, zhHans } from "vuetify/locale";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "@mdi/font/css/materialdesignicons.css";

export default createVuetify({
  components: {
    ...components,
    //VDataTable
  },
  directives,
  //  blueprint: md1,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
  locale: {
    locale: "zhHans",
    messages: { zhHans, pl },
  },

  theme: {
    themes: {
      light: {
        dark: false,
        colors: {
          color1: "#CA0808", //decToHex(202,8,8),
          color2: "#B21919",
          color3: "#B33232",
          color4: "#891F1F",
          color5: "#33333F",
          color6: "#6E6E76",
          color7: "#766E6E",
          color8: "#524040",
          color9: "#5F2817",
          color10: "#D98640",
        },
      },
    },
  },
});
