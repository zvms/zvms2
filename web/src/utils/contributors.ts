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
    infoHtml: `<style>
		body {
			background-color: #252525;
			margin: 0;
			padding: 0;
			display: flex;
			align-items: center;
			justify-content: center;
			height:100vh;
		}

		h1 {
			color: #000000;
			font-family: "STKaiti", sans-serif;
			font-weight: bold;
			text-align: center;
			font-size: 6vw;
			padding: 0.25em;
			line-height:1;
			animation: pop-up 2s ease-out forwards infinite alternate;
			text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
      		cursor: pointer;
      		border: none;
      		outline:none;
		}

		h1:hover {
			text-shadow:none;
			transform: rotateY(360deg);
		}
		
		@keyframes pop-up {
			from {
				transform: scale(0.5);
				opacity: 0;
			}
			to {
				transform: scale(1);
				opacity: 1;
			}
		}
	</style><h1>这是周济睿<br>文档编写以及流程测试<br>纯合致死<br>不啻微芒，造炬成阳</h1>` ,
  },
} satisfies Record<string, Contributor>;
