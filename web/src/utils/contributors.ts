import slcImage from "@/assets/slcw.webp"

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
Zecyel, SOF-Architect, Zest Programmer.<br/>
See: github.com/zecyel <img src="https://img.shields.io/badge/-@zecyel-181717?style=for-the-badge&logo=github&logoColor=white"/><br/>
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
    <img src="${slcImage}" width="130"/>`,
  },
  {
    displayName: "Solecour",
    infoHtml: `<p>2021级 黄瀚霆</p>`,
  },
  {
    displayName: "dblark",
    infoHtml: `2021级 周圣杰`,
  },
] satisfies Contributor[];

export const contributorsV2 = [
  {
    displayName: "qnc",
    infoHtml: `2022级 邱念楚 <br/> 关注<a href="http://172.31.2.4:19198">define-syntax.org</a>`,
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
    infoHtml: `
    <h2><p>是周济睿，我想应该不用介绍了、</p>
    <p>文档编写以及流程测试纯合致死</p>
    <p>不啻微芒，造炬成阳</p></h2>

    <style>
   h2 {
  font-size: 40px;
  color: #fff;
  text-align: center;
  text-transform: uppercase;
  position: relative;
  background: linear-gradient(90deg, #1d2128, #787878);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: glitch 3s ease-in-out infinite;
}

@keyframes glitch {
  0% {
    transform: skew(0.5deg, 0.1deg) translate(0, 0);
  }
  10% {
    transform: skew(0.5deg, -0.05deg) translate(5px, -5px);
  }
  20% {
    transform: skew(0.1deg, 0.2deg) translate(-5px, 5px);
  }
  30% {
    transform: skew(-0.2deg, 0.4deg) translate(10px, -10px);
  }
  40% {
    transform: skew(-0.7deg, -0.5deg) translate(-10px, 10px);
  }
  50% {
    transform: skew(0.55deg, -0.15deg) translate(15px, -15px);
  }
  60% {
    transform: skew(-0.25deg, 0.3deg) translate(-15px, 15px);
  }
  70% {
    transform: skew(0.35deg, -0.45deg) translate(20px, -20px);
  }
  80% {
    transform: skew(-0.15deg, 0.1deg) translate(-20px, 20px);
  }
  90% {
    transform: skew(0.2deg, -0.3deg) translate(25px, -25px);
  }
  100% {
    transform: skew(0.5deg, -0.1deg) translate(-25px, 25px);
  }
}

  
    </style>
    
` ,
  },
} satisfies Record<string, Contributor>;
