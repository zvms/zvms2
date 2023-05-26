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

// a temporary fix for pinia-plugin-persist
import { type PiniaPluginContext } from 'pinia';
export interface PersistStrategy {
    key?: string;
    storage?: Storage;
    paths?: string[];
}
export interface PersistOptions {
    enabled: true;
    strategies?: PersistStrategy[];
}
declare type Store = PiniaPluginContext['store'];
declare module 'pinia' {
    interface DefineStoreOptionsBase<S, Store> {
        persist?: PersistOptions;
    }
}