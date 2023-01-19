import { createEnums, int } from "zvms-apis-types-gen";

export const enums = createEnums({
    VolType: {
        _type: int(),
        _pyEnumType: "IntEnum",
        INSIDE: 1,
        OUTSIDE: 2,
        LARGE: 3
    },
    VolStatus: {
        _type: int(),
        _pyEnumType: "IntEnum",
        UNAUDITED: 1,
        AUDITED: 2
    },
    ThoughtStatus: {
        _type: int(),
        _pyEnumType: "IntEnum",
        WAITING_FOR_SIGNUP_AUDIT: 1,
        UNSUBMITTED: 2,
        DRAFT: 3,
        WAITING_FOR_FIRST_AUDIT: 4,
        WAITING_FOR_FINAL_AUDIT: 5,
        ACCEPTED: 6,
        REJECTED: 7,
    },
    NoticeType: {
        _type: int(),
        _pyEnumType: "IntEnum",
        USER_NOTICE: 1,
        CLASS_NOTICE: 2,
        SCHOOL_NOTICE: 3,
    }
});
