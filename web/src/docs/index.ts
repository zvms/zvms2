import index from "./content";

export type DocContent = string;

// Raw doc data
export interface Doc {
  name: string;
  title: string;
  content: DocContent;
  children: Doc[];
}

export interface DocItem {
  name: string;
  path: string[];
  title: string;
  content: DocContent;
  children: DocItem[];
}

type DocIndex = Record<string, DocItem>;

export function generateDoc(
  doc: Doc,
  currentPath: string[],
  index: DocIndex
): DocItem {
  const docItem = {
    name: doc.name,
    path: currentPath,
    title: doc.title,
    content: doc.content,
    children: doc.children.map((c) =>
      generateDoc(c, currentPath.concat([doc.name]), index)
    ),
  } satisfies DocItem;
  index[doc.name] = docItem;
  return docItem;
}

export function generateDocs(): DocIndex {
  let docIndex: DocIndex = {};
  generateDoc(index, [], docIndex);
  return docIndex;
}

export const docs = generateDocs();
