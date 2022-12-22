import { applyNavItems } from "../../utils/nav.js";
import { toasts } from "../../utils/dialogs";
import router from "../../router";
import { useInfoStore, useLastseenvolStore } from "@/stores";

export async function logout() {
    let res = {
        data: {
            "type": "SUCCESS",
            "message": "登出成功"
        }
    }
    toasts.success(res.data.message);

    this.infoStore.$reset();
    useLastseenvolStore().$reset();

    router.push("/login");

    applyNavItems();
    return res;
}
