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
    infoHtml: `<span>2021级 沈乐宸</span><br/>
    Linux enthusiast.<br/>
    <img src="https://img.shields.io/badge/-@So1aric-181717?style=for-the-badge&logo=github&logoColor=white"/><br/>
    <img src="src/assets/slcw.webp" width="130"/>`,
  },
  {
    displayName: "Solecour",
    infoHtml: `2021级 黄瀚霆`,
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
    infoHtml: `2022级 陈浏畅<br/>一只蒟蒻`,
  },
] satisfies Contributor[];

export const contributorsOther = {
  zsz: {
    displayName: "zsz",
    infoHtml: `2022级 张圣泽
政宣部成员`,
  },
  _7086cmd: {
    displayName: "7086cmd",
    infoHtml: `蛟川书院 初三 吴承宇<br/>
github.com/7086cmd`,
  },
  zjr: {
    displayName: "zjr",
    infoHtml: `是周济睿，我想应该不用介绍了、`,
  },
} satisfies Record<string, Contributor>;
