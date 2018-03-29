nodepy
====
状态
----
  脚手架 状态，暂不可用.现在主要使用dev&learn（默认分支）(暂时不往 master中合并)
基本描述
--------
  以相对布局和节点为核心的GUI框架，主要为了快速实现demo。
目标 是 做 一个 自己 用着 顺手，适合 新手 的 python GUI框架(参照kivy)
在 kivy 的 基础上 进行 简化，边学习 边加入 自己 的 想法。
环境及依赖
---------
  Windows 10 64bit
  Kivy：v1.10.1.dev0, git-5f62b6b, 20180103
  Python：v3.6.4 (v3.6.4:d48eceb, Dec 19 2017, 06:54:40) [MSC v.1900 64 bit (AMD64)]
注意
----
  nodepy 使用 右手坐标系(left-top)（但是 kivy 本身 使用 左手坐标系(right-bottom)）.
  nodepy 各ui组件的 pos 及 size 均为 相对值。
  为了 更简单的使用，提供的功能很简单。
  如果追求更丰富的功能，推荐直接使用 kivy 等更全面的框架(不推荐在nodepy中直接使用kivy)。
