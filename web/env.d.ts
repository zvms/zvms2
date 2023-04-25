/// <reference types="vite/client" />

declare interface DocModule {
  attributes: {
    name: string;
    title: string;
  };

  html: string;

  children?: DocModule[];
}

declare module "*.md" {
  const attributes: {
    name: string;
    title: string;
  };

  const html: string;

  export { attributes, html };
}
