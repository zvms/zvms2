export interface Type {
    desc?: Description;
    ts: string;
    py: string;
}

export type Description = string;

export type GenFunc = (params: any) => Type;

export const typesIndexRaw=
`export * from "./structs";`