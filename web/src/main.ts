import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersist from 'pinia-plugin-persist';

import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";

import "./assets/main.css";
import "./style.css";

const app = createApp(App);

app.use(createPinia().use(piniaPluginPersist));
app.use(router);
app.use(vuetify);

app.mount("#app");
