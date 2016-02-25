# VirtualJudgePY
基于 tornado 框架的 virtual judge
-----

![Screenshot from 2016-02-25 15:23:57.png](https://ooo.0o0.ooo/2016/02/25/56cead3b989b3.png)

![Screenshot from 2016-02-25 15:26:25.png](https://ooo.0o0.ooo/2016/02/25/56cead3ec0845.png)

![Screenshot from 2016-02-25 15:25:28.png](https://ooo.0o0.ooo/2016/02/25/56cead4298ecf.png)

![Screenshot from 2016-02-25 15:24:40.png](https://ooo.0o0.ooo/2016/02/25/56cead42bf6c3.png)

![Screenshot from 2016-02-25 15:25:01.png](https://ooo.0o0.ooo/2016/02/25/56cead4346d51.png)


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

# 更多OJ支持开发中...