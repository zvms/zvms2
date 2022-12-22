//import '@fortawesome/fontawesome-free/css/all.css'
import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue';
import Vuetify from 'vuetify/lib';


Vue.use(Vuetify)
Vuetify.config.silent = false;

const opts = {
    icons: {
        iconfont: 'mdi',
        //iconfont: 'fa'
    },
    theme: {
        themes: {
            "light": { "primary": "#92BAEE" },
            "dark": { "primary": "#424242" }
        },
    },
}
export default new Vuetify(opts)