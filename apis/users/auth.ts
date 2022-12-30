import { userCatagories } from "./catagories.js";
import { AuthData } from "zvms-apis-users-gen";

const {
    none,
    student
} = userCatagories.raw;

const {
    except
} = userCatagories

export const authData = {
    mePageOnNav: except(none),
    abc: [student]
} as const;