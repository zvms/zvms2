import * as content from './content';

export type DocContent = string;

export interface DocItem {
  name: string;
  path: string[];
  urlPath: string;
  title: string;
  content: DocContent;
  children: DocItem[];
}

type DocIndex = Record<string, DocItem>;

function generateDoc(
  doc: DocModule,
  currentPath: string[],
  docIndex: DocIndex
): DocItem {
  const docItem = {
    name: doc.attributes.name,
    path: currentPath,
    urlPath: `/docs/${doc.attributes.name}`,
    title: doc.attributes.title,
    content: doc.html,
    children: doc.children?.map((c) =>
      generateDoc(c, currentPath.concat([doc.attributes.name]), docIndex)
    ) ?? [],
  } satisfies DocItem;
  docIndex[doc.attributes.name] = docItem;
  return docItem;
}

export function generateDocs(): DocIndex {
  let docIndex: DocIndex = {};
  generateDoc(content, [], docIndex);
  return docIndex;
}

export const docs = generateDocs();
