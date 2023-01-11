export * from "./common.js";
export * from "./structs.js";
export * from "./types.js";
export * from "./enum.js";

export const typesIndexRaw =
    `export * from "./structs.js";
export * from "./enums.js";`;

export const typesInitRaw =
    `__ALL__ = [
    "./structs",
    "./structs_ck",
    "./enum"
]
`;