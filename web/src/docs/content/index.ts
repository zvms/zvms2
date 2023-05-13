export * from "./content.md";

import * as appendix from "./appendix";
import * as auditor from "./auditor";
import * as classleader from "./classleader";
import * as commonStudents from "./common_students";
import * as flowchart from "./flowchart";
import * as rule from "./rule";
import * as studentsUnion from "./students_union";
import * as teacher from "./teacher";

export const children = [
  flowchart,
  commonStudents,
  classleader,
  studentsUnion,
  //auditor,
  appendix,
  rule,
];
