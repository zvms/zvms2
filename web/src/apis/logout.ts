import { applyNavItems } from "../utils/nav.js";
import Axios from "axios";
import { toasts } from "../utils/dialogs";
import router from "../router";
import { useInfoStore, useLastseenvolStore } from "@/stores";


export async function logout() {
    try {
        try {
            let res = await Axios.post("/user/logout");
            if (res?.data?.type !== "SUCCESS") {
                throw new Error(res?.data?.message);
            }
            toasts.success(res.data.message);
        } catch (e :any) {
            toasts.error(e.message);
            throw e;
        }

        this.infoStore.$reset();
        useLastseenvolStore().$reset();

        applyNavItems();
        router.push("/login");
    } catch {
        return false;
    }
    return true;
}