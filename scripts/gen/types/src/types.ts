export interface Type {
    desc?: Description;
    ts: string;
    py: string;
    ck: string; //Python runtime type checking
}

export type Description = string;

export type GenFunc = (params: any) => Type;

export const typesIndexRaw =
    `export * from "./structs.js";`;

export const typesInitRaw =
    `__ALL__ = [
    "./structs",
    "./structs_ck",
    "./enum"
]
`;