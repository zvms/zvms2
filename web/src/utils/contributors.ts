export interface Contributor {
  displayName: string;
  infoHtml: string;
}

export const contributorsV1 = [
  {
    displayName: "张子苏",
    infoHtml: `2018级 张子苏`,
  },
  {
    displayName: "neko_moyi",
    infoHtml: `2019级 卢锦轩`,
  },
  {
    displayName: "Zecyel",
    infoHtml: `2020级 朱程炀<br/>
Zecyel, SOF-Architect,<br/>
Zest Programmer.<br/>
See: github.com/zecyel<br/>
Star every repo you find!`,
  },
  {
    displayName: "fpc5719",
    infoHtml: `2020级 陈琛`,
  },
  {
    displayName: "So1aric",
    infoHtml: `2021级 沈乐宸`,
  },
  {
    displayName: "Solecour",
    infoHtml: `2021级 黄瀚庭`,
  },
  {
    displayName: "dblark",
    infoHtml: `2021级 周圣杰`,
  },
] satisfies Contributor[];

export const contributorsV2 = [
  {
    displayName: "qnc",
    infoHtml: `2022级 邱念楚`,
  },
  {
    displayName: "_Kerman_xtr",
    infoHtml: `2022级 熊桐睿<br/>
    <i>_Kerman is async</i><br/>
    <img src="https://img.shields.io/badge/-@KermanX-181717?style=flat-square&logo=github&logoColor=white"/><br/>
    <img src="https://img.shields.io/badge/-@UniCoderGroup-181717?style=flat-square&logo=github&logoColor=white"/><br/>
    <img src="https://img.shields.io/badge/-@Structure--oriented_Framework-181717?style=flat-square&logo=github&logoColor=white"/><br/>
    <img src="https://img.shields.io/badge/-KermanX@qq.com-168de2?style=flat-square&logo=mail.ru&logoColor=white"/>
    `,
  },
  {
    displayName: "clc",
    infoHtml: `2022级 陈浏畅`,
  },
] satisfies Contributor[];

export const contributorsOther = {
  zsz: {
    displayName: "zsz",
    infoHtml: ``,
  },
} satisfies Record<string, Contributor>;
