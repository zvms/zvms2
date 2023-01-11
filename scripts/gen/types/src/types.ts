export interface Type {
    desc?: Description;
    ts: string;
    py: string;
    ck: string; //Python runtime type checking
}

export type Description = string;

export type GenFunc = (params: any) => Type;