import slcImage from "@/assets/slcw.webp";
import iconUrl from "@/assets/favicon.ico";
import clcImage from "@/assets/clcshinano.gif";

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
<img src="https://foruda.gitee.com/avatar/1677005889603604423/2133909_zhuchengyang_1604067001.png!avatar200"/>
<br/>
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
    <a href="http://172.31.2.4:16541">Linux enthusiast.</a><br/>
    <img src="https://img.shields.io/badge/-@So1aric-181717?style=for-the-badge&logo=github&logoColor=white"/><br/>
    <img src="${slcImage}" width="130" />`,
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
    displayName: "_Kerman",
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
    infoHtml: `2022级 陈浏畅<br/>
    一只蒟蒻<br/>
    <img src="${clcImage}" width="240" height="201" lazy><br/>`,
  },
  {
    displayName: "7086cmd",
    infoHtml: `2023级 吴承宇<br/>
github.com/7086cmd|逸一时误一世，逸久逸久 Bug 已零|大 Bug 病了二 Bug 瞧，三 Bug 采药四 Bug 嗷|菜到除了头全是#00FF00`,
  },
  {
    displayName: "byh",
    infoHtml: `2023级 鲍屹涵<br/>`,
  },
] satisfies Contributor[];

export const contributorsOther = {
  hhj:{
    displayName: "hhj",
    infoHtml: `2022级 黄浩杰<br/>
    <style>
        /* 添加彩虹动画 */
        @keyframes rainbow {
            0%   {color: red;}
            16%  {color: orange;}
            33%  {color: yellow;}
            50%  {color: green;}
            66%  {color: blue;}
            83%  {color: indigo;}
            100% {color: violet;}
        }

        /* 添加动画效果 */
        .rainbow-text {
            animation: rainbow 2s infinite;
        }
    </style>
    <h1 class="rainbow-text">黄浩杰的自我介绍</h1>
    <p>我是黄浩杰，来自2023级5班。</p>
    <p>我的个人博客可以在 010305.xyz 找到。</p>
    <p>如果你想联系我，可以通过QQ：2648616832。</p>
    <p> <img src="https://010305.xyz/hhj.jpg"/> </p>`
  },
  zsz: {
    displayName: "zsz",
    infoHtml: `2022级 张圣泽
政宣部成员<br/>
<img src="${iconUrl}" width="300px" class="pt-2" />`,
  },
  zjr: {
    displayName: "zjr",
    infoHtml: `<style>
    div.zjr {
      background-color: #252525;
        margin: 0;
        padding: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        height:100vh;
      }

		h1.zjr {
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

		h1.zjr:hover {
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
	</style><div class="zjr"><h1 class="zjr">这是周济睿<br>文档编写以及流程测试<br>纯合致死<br>不啻微芒，造炬成阳</h1></div>`,
  },
} satisfies Record<string, Contributor>;
