import * as content from "./content";

export type DocContent = string;

export interface DocItem {
  name: string;
  path: string[];
  urlPath: string;
  title: string;
  content: DocContent;

  parent: DocItem | null;
  children: DocItem[];
}

type DocIndex = Record<string, DocItem>;

function generateDoc(
  doc: DocModule,
  parent: DocItem | null,
  currentPath: string[],
  docIndex: DocIndex
): DocItem {
  let docItemWithoutChildren = {
    name: doc.attributes.name,
    path: currentPath,
    urlPath: `/docs/${doc.attributes.name}`,
    title: doc.attributes.title,
    content: doc.html,
    parent,
  } as Omit<DocItem, "children">;
  const docItem = docItemWithoutChildren as DocItem;
  docItem.children =
    doc.children?.map((c) =>
      generateDoc(
        c,
        docItem,
        currentPath.concat([doc.attributes.name]),
        docIndex
      )
    ) ?? [];
  docIndex[doc.attributes.name] = docItem;
  return docItem;
}

export function generateDocs(): DocIndex {
  let docIndex: DocIndex = {};
  generateDoc(content, null, [], docIndex);
  return docIndex;
}

export const docs = generateDocs();
