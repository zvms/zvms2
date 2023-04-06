import "vuetify/styles";
import { createVuetify } from "vuetify";
import { pl, zhHans } from "vuetify/locale";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { md1 } from "vuetify/blueprints";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "@mdi/font/css/materialdesignicons.css";
//import { VDataTable } from "vuetify/labs/VDataTable";

/*
function decToHex(r: number,g: number,b: number) {
  return '#'+;
}
*/

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
  /*
  202 8 8 
  178 25 25
  179 50 50
  137 31 31

  51 51 63
  110 110 118
  118 118 110
  82 64 64
  95 40 23
  217 134 64
  */
});
