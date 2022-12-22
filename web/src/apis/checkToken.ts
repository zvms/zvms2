import Axios from "axios";
import {logout} from "./logout";

export async function checkToken(/*unknown_arg x1 */) {
    try {
        let res = await Axios.post("/user/info");
        if (res.data.type != "SUCCESS") {
            throw res.data.message;
        }
    } catch {
        await logout();
    }
}