import { createEnums, int } from "zvms-apis-types-gen";

export const enums = createEnums({
    VolType: {
        _type: int(),
        INSIDE: 1,
        OUTSIDE: 2,
        LARGE: 3
    }
})