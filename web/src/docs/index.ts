export interface DocItem {
  title: string;
  contentHtml: string;
  children: DocItem[];
}

const docIndex = {
  title: "帮助文档",
  contentHtml: "1222",
  children: [],
} satisfies DocItem;

export const docs = {
  index: docIndex,
} satisfies Record<string, DocItem>;
