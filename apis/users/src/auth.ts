import { userCatagories } from "./catagories.js";
import { AuthData } from "zvms-apis-users-gen";

const {
    none,
    student
} = userCatagories.raw;

const {
    except
} = userCatagories

export const authData: AuthData = {
    mePageOnNav: except(none),
    abc: [student]
}   
