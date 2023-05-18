import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersist from "pinia-plugin-persist";

import App from "@/App.vue";
import router from "@/router";
import vuetify from "@/plugins/vuetify";

import "@/assets/main.css";
import "@/style.css";
import { toasts } from "./utils/dialogs";

export const VERSION = "v2.0.2"

const app = createApp(App);

app.use(createPinia().use(piniaPluginPersist));
app.use(router);
app.use(vuetify);

app.mount("#app");

window.addEventListener("error", (ev) => {
  toasts.error(`前端出错啦！
        ${ev.filename}第${ev.lineno}行第${ev.colno}列：${ev.error}`);
  return false;
});
