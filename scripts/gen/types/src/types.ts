export interface Type {
    desc?: Description;
    ts: string;
    py: string;
    ck: string; //Python runtime type checking
}

export type Description = string;

export type GenFunc = (params: any) => Type;

export const typesIndexRaw =
    `export * from "./structs";`

export const typesInitRaw =
    `export * from "./structs";`