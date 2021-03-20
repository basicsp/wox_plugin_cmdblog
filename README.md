# plugin for wox

## 用途：

本项目是wox的插件，利用github作为自己的知识仓库，使用wox快速查询。

作者：perrysun82@github.com
wox地址：http://wox.one

## 知识库：

知识库分两级，按目录组织，内部要有readme.md，注意：必须markdown的一级标题

仓库案例地址：https://github.com/basicsp/cmdblog/tree/master/

## 安装：

本项目下载为zip文件，后缀名修改为wox；打开wox，拖入搜索框，点击确认安装。

python项目每次由wox调用时会重新加载，修改py文件可以即时生效，调试方便。

wox里需要制定Python的安装位置为：D:\Anaconda3

如果pip出错，执行：python -m ensurepip    python -m pip install --upgrade pip

如果插件不执行，请查看cmd_error.log文件，多半是缺少以下两个库：

pip install clipboard

pip install markdown_to_json

## 用法：

cb update：把github仓库down到当前目录cmdblog中，后续均为本地搜索。

![1567244533777](./icon/r0.png)

![1567243677089](./icon/r1.png)

![1567243873704](./icon/r2.png)

![1567243840843](./icon/r3.png)

