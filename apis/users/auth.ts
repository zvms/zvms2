import { userCatagories } from "./catagories.js";
import { AuthData, createUserOrder } from "zvms-apis-users-gen";

const {
    none,
    student,
    teacher,
    aclass,
    manager,
    auditor,
    system
} = userCatagories.raw;

const {
    except
} = userCatagories;

const logined = except(none);

const mainOrder = createUserOrder(
    none,
    student,
    aclass,
    teacher,
    manager,
    auditor,
    system
);

const all = [none, student, teacher, aclass, manager, auditor, system];
const classManager = mainOrder.overEqual(aclass);
const schoolManager = mainOrder.overEqual(teacher);

export const authData = {
    mePageOnNav: logined,

    login: [none],
    auditSignup: [auditor],
    rollbackSignup: [auditor],

    readSchoolNotice: all,
    writeSchoolNotice: schoolManager,
    readClassNotice: logined,
    writeClassNotice: classManager,
    readAnyNotice: schoolManager,
    writeAnyNotice: schoolManager,

    readMyVol: logined,
    writeMyVol: logined,
    readClassVol: classManager,
    writeClassVol: classManager,
    readAnyVol: schoolManager,
    writeAnyVol: schoolManager,

    readMyUserInfo: logined,
    readClassUserInfo: classManager,
    readAnyUserInfo: schoolManager,
    writeUserInfo: schoolManager,

    readAnyClass: schoolManager,
    writeClass: schoolManager,

} as const;