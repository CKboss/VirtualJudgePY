# VirtualJudgePY
基于 tornado 框架的 virtual judge
-----

```shell
 _    ___      __              __    __          __           ______  __
| |  / (_)____/ /___  ______ _/ /   / /_  ______/ /___ ____  / __ \ \/ /
| | / / / ___/ __/ / / / __ `/ /_  / / / / / __  / __ `/ _ \/ /_/ /\  / 
| |/ / / /  / /_/ /_/ / /_/ / / /_/ / /_/ / /_/ / /_/ /  __/ ____/ / /  
|___/_/_/   \__/\__,_/\__,_/_/\____/\__,_/\__,_/\__, /\___/_/     /_/   
                                               /____/ v0.1.2
```

![首页](http://ww1.sinaimg.cn/mw1024/50a04a61gw1f1xwn7vsqdj21330qhth1.jpg)


------

# 安装:

#### VirtualJudgePY 依赖以下python包:

```python

tornado 4.3

pymysql 0.7.1

beautifulsoup4 4.4

sqlalchemy 1.0.1

```

#### OJ账号配置:

在Crawler下各个OJ的Config文件下,账号格式为login时post的数据的格式

#### 数据库配置:

数据库表见 ```sql_version_1_2.sql```

可在tools.dbcore里配置数据库连接


#### 路径配置和参数配置:

在Config包对应文件下配置,

FilePathConfig 可以设置VirtualJudgePY会在运行时生成的一些临时的pkl文件存放位置
ParametersConfig 可以配置一些临时线程池的大小


#### OJ题目抓取和题目导入

目前可以支持的OJ有 : PKU,HDU,ZOJ,BZOJ

在各个OJ的Cawler中可以指定抓取的题目范围,并储存为pkl文件,用tools里的ImportProblem来将pkl文件导入数据库

------


# 运行

```python
python3 __init__.py
```

------

# OJ抓取配置

virtualjudgePY中新增加OJ支持非常的容易

### 1. 新增OJ包添加到Crawler下.

每个OJ抓取包括一下几个部分: 

* Config设置账号和登陆post数据格式,

* Crawler抓取题目,下载一个题目的网页,并从中取得 数据库表problem和problemdetail表中的部分或全部的列,然后存为PKL文件.

* Scanner扫描OJ的status列表并返回list格式的结果

* Vjudge,登陆oj后用post提交题目

具体内容可以参考BzojCrawler

### 2. 在Crawler.Config的AutoSubmit中设置新OJ的提交调用的Vjudge

### 3. 在MainScanner中添加新OJ的SCanner

### 4. 在ParametesConfig的OJ列表中中添加新OJ的名称

#### Contest功能暂不完善,更多OJ支持开发中...