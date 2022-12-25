import { Type, Description } from "zvms-apis-types-gen";
import { AuthData } from "zvms-apis-users-gen";
export { Type, Description };

export interface Apis {
    [partPath: string]: Part;
}

export interface Part {
    paths: Paths;
    desc?: Description;
    cfg?: Config;
}

export type PathItem = string;

export interface Paths {
    [pathItem: PathItem]: Path;
}

export interface Path {
    paths?: Paths;
    desc?: Description;
    get?: Method;
    post?: Method;
    cfg?: Config
}

export interface Method {
    name:string;
    desc?: Description;
    req?: Params;
    res?: Params;
    _req?: DefaultParams;
    _res?: DefaultParams;
    cfg?: Config;
    auths?: (AuthData[0])[];
}

export interface Params {
    [key: string]: Type;
}

export interface Config {
    token?: boolean;
}

export interface DefaultParams {
    [key: string]: unknown;
}

export type ImplFile = string;

export type ImplFiles = Record<string, ImplFile>;