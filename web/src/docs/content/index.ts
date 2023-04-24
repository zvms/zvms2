import type { Doc } from "@/docs";
import auditor from "./auditor";

const index = {
    name: "index",
  title: "帮助文档",
  content: "1222",
  children: [
    auditor
  ],
} satisfies Doc;

export default index;
