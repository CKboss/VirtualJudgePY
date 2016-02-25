# VirtualJudgePY
基于 tornado 框架的 virtual judge
-----

![首页](http://ww1.sinaimg.cn/mw1024/50a04a61jw1f1bmfi7zenj213j0p0q6y.jpg)

![ProblemList](http://ww1.sinaimg.cn/mw1024/50a04a61jw1f1bmfiszqzj214x0skdsl.jpg)

![Problem](http://ww4.sinaimg.cn/mw1024/50a04a61jw1f1bmfl7ay1j213f0sk146.jpg)

![Status](http://ww1.sinaimg.cn/mw1024/50a04a61jw1f1bmfjo3ogj214x0sk4df.jpg)

![Contest](http://ww4.sinaimg.cn/mw1024/50a04a61jw1f1bmfka4apj214x0sktkj.jpg)

![Create Contest](http://ww1.sinaimg.cn/mw1024/50a04a61jw1f1bmfkpu19j213f0skwju.jpg)


------

# 安装:

#### VirtualJudgePY 依赖:

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

在tools.dbcore里配置数据库连接


#### 路径配置和参数配置:

在Config包对应文件下配置


#### OJ题目抓取和题目导入

目前可以支持的OJ有 : PKU,HDU,ZOJ

在各个OJ的Cawler中可以指定抓取的题目范围,并储存为pkl文件,用tools里的ImportProblem来将pkl文件导入数据库

------


# 运行

```python
python3 __init__.py
```

------

# Contest暂不完善,更多OJ支持开发中...