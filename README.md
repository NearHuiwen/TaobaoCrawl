淘宝根据搜索词爬取商品爬虫，无selenium，动态cookie
===============

> 项目普及技术：Scrapy、MySql

请在Python3下运行(版本太低可能会出现不兼容，本人用的是3.7版本)

运行前请配置好MySql相关数据
数据库脚本在文件里，数据库名：taobao

## 注意
目前淘宝爬虫大多数使用selenium获取cookie后爬取

本人核心思路是使用cookie池动态请求接口，请求延迟是2秒，获取相关商品信息，亲测爬取成功（当时使用仅用一个cookie，当然数据越多失效机率越大）

如果使用分布式最好有动态IP，cookie也可以专门有一台机器爬取cookie

（截止版本2020年11月27日，即后面可能接口出现更新，可能会过时，请谅解）

源码仅作为和大家一起**学习Python**使用，你可以免费: 拷贝、分发和派生当前源码。

但你用于*商业目的*及其他*恶意用途*，作者也不会管你，耗子尾汁





## 开发环境安装

首先，配置好你的Python、MySql环境

本人用的是pipenv虚拟环境
如果你已有虚拟环境以下可忽略
安装
```bash
$ pip install -i https://pypi.douban.com/simple pipenv
```
创建文件夹“TaobaoCrawl”（项目放在这里）
创建虚拟环境
```bash
$ cd TaobaoCrawl
$ pipenv install
```

进入虚拟环境
```bash
$ cd TaobaoCrawl
$ pipenv shell
```



导入项目，也可直接下载覆盖TaobaoCrawl文件夹
```bash
$ git clone https://github.com/NearHuiwen/TaobaoCrawl.git
```


大功告成,直接跳到下一节配置和运行.

## 配置和运行

首先部署MySql数据库

数据库脚本在文件里，数据库名：taobao

在db_manager_mysql.py 配置MySql账号和密码

## 运行步骤：

1、登录淘宝后，随便搜索点东西，获取cookie如下图

<img src="https://raw.githubusercontent.com/NearHuiwen/TaobaoCrawl/master/picture/a.png" width="700">

当然你也可以使用selenium动态登录获取

在cookie_utils.py 配置至少一个cookie

2、在goods.py 填入需要搜索商品的搜索词，我用的是：self.search_word_list=["眼镜","面霜"]

3、运行main.py 即可爬取信息

4、在setting.py 可配置：DOWNLOAD_DELAY = 2#接口请求延迟（太快容易被封号）

## 数据库展示如下：

<img src="https://raw.githubusercontent.com/NearHuiwen/TaobaoCrawl/master/picture/b.png" width="700">



