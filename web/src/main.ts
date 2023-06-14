import "core-js/stable/array/at"; // polyfill for Array.prototype.at used in v-data-table component.

import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersist from "pinia-plugin-persist"; //@ts-ignore

import App from "@/App.vue";
import router from "@/router";
import vuetify from "@/plugins/vuetify";

import "@/assets/main.css";

import { registerTelemetry } from "@/utils/telemetry";

export const VERSION = "v2.0.2";

const app = createApp(App);

app.use(createPinia().use(piniaPluginPersist));
app.use(router);
app.use(vuetify);

app.mount("#app");

registerTelemetry();
