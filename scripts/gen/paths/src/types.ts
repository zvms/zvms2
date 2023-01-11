import { Type, Description } from "zvms-apis-types-gen";
import { UserCatagoryList, UserCatagory } from "zvms-apis-users-gen";
export { Type, Description };

export type MethodName =
    | "GET"
    | "POST"
    | "PUT"
    | "DELETE"
    | "PATCH";
export type Params = {
    [key: string]: Type;
};
export interface DefaultParams {
    [key: string]: unknown;
}
export interface Method {
    name: string;
    type: MethodName,
    desc?: Description;
    auths?: UserCatagoryList[];
    req?: Params;
    res?: Params;
    _req?: DefaultParams;
    _res?: DefaultParams;
}

type AllowedPathCharLowercase =
    | "a" | "b" | "c" | "d" | "e"
    | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
    | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u"
    | "v" | "w" | "x" | "y" | "z";
type AllowedPathCharUppercase = Uppercase<AllowedPathCharLowercase>;
type AllowedPathCharSpecial =
    | "-" | "_"
    | "<" | ">" | ":";
type AllowedPathChar =
    | AllowedPathCharLowercase
    | AllowedPathCharUppercase
    | AllowedPathCharSpecial;
export type PathItemName
    <S extends string, S0 extends string = S>
    = S extends `${AllowedPathChar}${infer S1}` ?
    S1 extends "" ?
    `/${S0}` : PathItemName<S1, S0>
    : never;
export interface PathItem {
    name: string,
    //desc: Description,
    //auth: UserCatagoryList[],
    methods: Method[],
    children: PathItem[]
}

export function $<S extends string>(
    name: PathItemName<S>,
    //desc: Description,
    //auth: UserCatagoryList[],
    ...etc: (Method | PathItem)[]
): PathItem {
    let methods: Method[] = [],
        children: PathItem[] = [];
    for (const v of etc) {
        if (Object.hasOwn(v, "type")) {
            const m = v as Method;
            methods.push(m);
        } else {
            const c = v as PathItem;
            children.push(c);
        }
    }
    return {
        name,
        //desc,
        //auth,
        methods,
        children
    }
}

export type Apis = PathItem[];

export type ImplFile = string;

export type ImplFiles = Record<string, ImplFile>;

export interface GenCtx {
    fileName: string,
    path: string
}

export type ImplCodes = Record<string, [code: string, used: boolean]>;