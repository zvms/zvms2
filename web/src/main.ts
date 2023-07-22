import "core-js/stable/array/at"; // polyfill for Array.prototype.at used in v-data-table component.

import { createApp } from "vue";
import { createPinia } from "pinia";

//@ts-ignore
import piniaPluginPersist from "pinia-plugin-persist";

import App from "@/App.vue";
import Router from "@/router";
import Vuetify from "@/plugins/vuetify";
import Toast, {options} from "@/plugins/toastification";

import "@/assets/main.css";
import 'animate.css/animate.min.css'

import { registerTelemetry } from "@/utils/telemetry";

const app = createApp(App);

app.use(createPinia().use(piniaPluginPersist));
app.use(Router);
app.use(Vuetify);
app.use(Toast, options);

app.mount("#app");

registerTelemetry();
