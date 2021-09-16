<div align="center">

# BiliLiveData

<!-- markdownlint-disable-next-line MD036 -->
_✨ 分布式 Bilibili直播间 数据监控与存储 ✨_

_✨ Author: NagisaCo ✨_
</div>

<p align="center">
  <a href="license">
    <img src="https://img.shields.io/badge/LICENSE-GPLv3-red" alt="license">
  </a>
  <a href="stargazers">
    <img src="https://img.shields.io/github/stars/NagisaCo/BiliLiveData?color=yellow&label=Github%20Stars" alt="star">
  </a>
  <img src="https://img.shields.io/badge/Python-3.9|3.8-blue" alt="python">
</p>
<!-- markdownlint-enable MD033 -->

<!-- vscode-markdown-toc -->
* 1. [简介](#)
	* 1.1. [特色](#-1)
* 2. [快速上手](#-1)
	* 2.1. [获取 BiliLiveData](#BiliLiveData)
	* 2.2. [服务端运行](#-1)
		* 2.2.1. [运行 Analysor.py](#Analysor.py)
		* 2.2.2. [配置 Analysor 配置文件](#Analysor)
	* 2.3. [收集端配置](#-1)
		* 2.3.1. [运行 Collector.py](#Collector.py)
		* 2.3.2. [配置 Collector 配置文件](#Collector)
* 3. [服务端环境搭建](#-1)
	* 3.1. [安装 RabbitMQ 消息队列](#RabbitMQ)
	* 3.2. [安装 MySQL 数据库](#MySQL)
	* 3.3. [安装 Redis 数据库](#Redis)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. <a name=''></a>简介

BiliLiveData 通过使用 [mosquito/aio-pika](https://github.com/mosquito/aio-pika) 模块搭配 [RabbitMQ](https://www.rabbitmq.com/) 消息队列进行分布式异步通信。

###  1.1. <a name='-1'></a>特色

收集端 `Collector` 采用 [MoyuScript/bilibili-api](https://github.com/MoyuScript/bilibili-api) b站 API 模块，收集指定直播间的用户状态、弹幕、礼物、SC、大航海等信息，并打包发送至 RabbitMQ 。

服务端 `Analysor` 使用 [aio-libs/aiomysql](https://github.com/aio-libs/aiomysql) 模块异步操作 [MySQL](https://www.mysql.com/) 数据库，使用 [jonathanslenders/asyncio-redis](https://github.com/jonathanslenders/asyncio-redis) 模块异步操作 [Redis](https://redis.io/) 数据库处理 RabbitMQ 中的数据。进行解压、去重后存入 MySQL 服务器中。

得益于 Python 的 [asyncio](https://docs.python.org/3/library/asyncio.html) 机制，BiliLiveData 处理事件的吞吐量有了很大的保障。再配合 RabbitMQ 消息队列，BiliLiveData 可实现多收集端共同收集直播数据，广范围高可靠性的收集数据。

##  2. <a name='-1'></a>快速上手

*由于可靠性与简便性需求，建议您将服务端 `Analysor` 配置在 Linux 服务器上*

###  2.1. <a name='BiliLiveData'></a>获取 BiliLiveData

首先使用以下指令安装本软件：

```shell
git clone https://github.com/NagisaCo/BiliLiveData.git
```

或者使用镜像源：

```shell
git clone https://hub.fastgit.org/NagisaCo/BiliLiveData.git
```

安装所需依赖：

```shell
cd BiliLiveData
python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

###  2.2. <a name='-1'></a>服务端运行

您需要在服务端配置可访问的 RabbitMQ 消息队列、 MySQL 数据库、 Redis 数据库服务。

如果您无相关配置，可按照后续步骤分别搭建 RabbitMQ 消息队列、 MySQL 数据库与 Redis 数据库，搭建过程详见[服务端环境搭建](#服务端环境搭建)

####  2.2.1. <a name='Analysor.py'></a>运行 Analysor.py

使用默认配置文件 `Analysor.conf`

```shell
python3 Analysor.py
```

或者指定conf配置文件

```shell
python3 Analysor.py --config YOUR_CONGIF_FILE
```

第一次运行会提示 `[config] file xxx.conf not found, already create default file` 并自动创建配置文件模板

> 使用 python3 Analysor.py --help 查看帮助

####  2.2.2. <a name='Analysor'></a>配置 Analysor 配置文件

1. 配置 MySQL 

    ```ini
    [mysql]  # mysql数据库配置
    host = localhost  # mysql服务器地址
    port = 3306  # mysql端口
    user = bili_live_data  # 登录用户
    password = bili_live_data  # 登录密码
    db = bili_live_data  # 使用数据库
    ```

2. 配置 Redis 

    ```ini
    [redis]  # redis数据库配置
    host = localhost  # redis服务器地址
    password =   # redis密码，无密码请留空
    port = 6379  # redis端口
    db = 2  # redis数据库
    ```

3. 配置 RabbitMQ 

    ```ini
    [rabbitmq]  # 消息队列配置
    host = localhost  # mq服务器地址
    port = 5672  # mq端口
    username = BiliLiveData  # mq用户名
    password = BiliLiveData  # mq密码
    virtualhost = /BiliLiveData  # mq virtual host
    queue_name = Data  # mq 队列名称
    ssl = False  # ssl启用
    ```

配置完成后可使用[运行 Analysor.py](#运行-analysorpy)步骤运行

您也可以使用 `screen` 后台运行程序

###  2.3. <a name='-1'></a>收集端配置

您需要在收集端配置可访问的 RabbitMQ 消息队列

####  2.3.1. <a name='Collector.py'></a>运行 Collector.py

使用默认配置文件 `Collector.conf`

```shell
python3 Collector.py
```

或者指定conf配置文件

```shell
python3 Collector.py --config YOUR_CONGIF_FILE
```

第一次运行会提示 `[config] file xxx.conf not found, already create default file` 并自动创建配置文件模板

> 使用 python3 Collector.py --help 查看帮助

####  2.3.2. <a name='Collector'></a>配置 Collector 配置文件

1. 配置 Container

    ```ini
    [container]  # 消息存放容器配置
    max_time = 300  # 容纳消息的时间跨度超过该值则发送
    max_num = 200  # 容纳消息的数量超过该值则发送
    ```

2. 配置 Listener

    ```ini
    [listener]  # 监听设置
    room_id_list = [21919321, 21919321]  # 所需监听的房间号列表
    ```

3. 配置 RabbitMQ 

    ```ini
    [rabbitmq]  # 消息队列配置
    host = localhost  # mq服务器地址
    port = 5672  # mq端口
    username = BiliLiveData  # mq用户名
    password = BiliLiveData  # mq密码
    virtualhost = /BiliLiveData  # mq virtual host
    queue_name = Data  # mq 队列名称
    ssl = False  # ssl启用
    )
    ```

配置完成后可使用[运行 Collector.py.py](#运行-collectorpy)步骤运行

您也可以使用 `screen` 后台运行程序

##  3. <a name='-1'></a>服务端环境搭建

###  3.1. <a name='RabbitMQ'></a>安装 RabbitMQ 消息队列

1. 安装 erlang 
   
    - 由于 RabbitMQ 需要 erlang 语言的支持，在安装 RabbitMQ 之前需要安装 erlang 。

    ```shell
    sudo apt-get update
    sudo apt-get install erlang-nox
    ```

2. 安装 RabbitMQ 
     
    ```shell
    sudo apt-get install rabbitmq-server
    ```

    - 启动、停止、重启、状态 RabbitMQ 命令

    ```shell
    sudo rabbitmq-server start
    sudo rabbitmq-server stop
    sudo rabbitmq-server restart
    sudo rabbitmqctl status
    ```

3. 配置 RabbitMQ 

    - 添加用户 `BiliLiveData` 与密码 `BiliLiveData` 

    ```shell
    sudo rabbitmqctl add_user BiliLiveData BiliLiveData
    ```

    - 为用户设置角色 `administrator`
    
    ```shell
    sudo rabbitmqctl set_user_tags BiliLiveData administrator
    ```

    - 添加 virtual host `/BiliLiveData` 

    ```shell
    sudo rabbitmqctl add_vhost /BiliLiveData
    ```

    - 为用户设置 virtual host

    ```shell
    sudo rabbitmqctl set_permissions -p /BiliLiveData BiliLiveData '.*' '.*' '.*'
    ```

    - 添加队列 `Data` 

    ```shell
    curl --location --request PUT 'http://localhost:15672/api/queues/%2FBiliLiveData/Data' \
    --header 'Authorization: Basic QmlsaUxpdmVEYXRhOkJpbGlMaXZlRGF0YQ==' \
    --header 'Content-Type: text/plain' \
    --data-raw '{"auto_delete":false,"durable":true,"arguments":{}}'
    ```


4. RabbitMQ Web GUI 使用

    - 安装了Rabbitmq后，默认也安装了 `rabbitmq_management` 管理工具，执行命令即可启动

    ```shell
    sudo rabbitmq-plugins enable rabbitmq_management
    ```

5. 开放端口

    - 开放 5672 数据端口与 15672 Web管理接口

    ```shell
    sudo iptables -I INPUT -p tcp --dport 5672 -j ACCEPT
    sudo iptables -I INPUT -p tcp --dport 15672 -j ACCEPT

    sudo iptables-save
    ```

    - 可使用 `iptables-persistent` 持续化保存规则

    ```
    sudo apt-get install iptables-persistent
    netfilter-persistent save
    netfilter-persistent reload
    ```

现在，您可以进入 http://your_server_ip:15672/ 查看与管理RabbitMQ

###  3.2. <a name='MySQL'></a>安装 MySQL 数据库

1. 安装 MySQL 8

    > Ubuntu在20.04版本中，源仓库中MySQL的默认版本已经更新到8.0。因此可以直接安装

    ```shell
    sudo apt-get update
    sudo apt-get install mysql-server
    ```

    - 安装完成后，可以通过下面的命令来查看运行状态

    ```shell
    systemctl status mysql
    ```

2. 进入 MySQL 

    - 进入 MySQL (密码无需输入 直接回车)

    ```shell
    mysql -u root -p
    ```

3. 配置 root 用户(可选)

    **MySQL 默认 root 用户没有密码, 但同时也无法远程使用 root 用户登录**

    - 切换 mysql 数据库

    ```sql
    USE mysql;
    ```

    - 设置 root 用户密码

    ```sql
    ALTER user 'root'@'localhost' identified WITH mysql_native_password BY '你自己的密码';
    flush privileges;
    ```

    - 设置 root 远程连接权限

    ```sql
    UPDATE user SET host='%' WHERE user='root';
    FLUSH PRIVILEGES;
    ```

4. 新增用户 `bili_live_data` 密码 `bili_live_data` 与 数据库 `bili_live_data`

    - 新增用户

    ```sql
    USE mysql;
    CREATE USER 'bili_live_data' IDENTIFIED BY 'bili_live_data';
    ```
    
    - 新增数据库
    
    ```sql
    CREATE DATABASE bili_live_data;
    ```

    - 新增权限

    ```sql
    GRANT all ON bili_live_data.* TO 'bili_live_data'@'%';
    FLUSH PRIVILEGES;
    ```

    - 可以通过以下命令查看所有用户与可访问 host (% 表示任意地址)

    ```sql
    SELECT host,user FROM user;
    ```

退出 MySQL 

```sql
QUIT
```

5. 开放 3306 端口(可选)

    > 开放外网访问 MySQL ，便于远程访问数据库

    - 配置 MySQL
    
        打开配置文件

        ```shell
        sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
        ```

        将bind-address = 127.0.0.1注销​

        ```
        # bind-address = 127.0.0.1
        ```

        使用 `:wq` 退出 vim 

        重启 linux

        ```shell
        sudo reboot
        ```

    - 配置防火墙

    ```shell
    sudo iptables -I INPUT -p tcp --dport 3306 -j ACCEPT
    sudo iptables-save
    ```

    - 可使用 `iptables-persistent` 持续化保存规则

    ```shell
    netfilter-persistent save
    netfilter-persistent reload
    ```


###  3.3. <a name='Redis'></a>安装 Redis 数据库

1. 安装 Redis

    ```shell
    sudo apt-get update
    sudo apt-get install redis-server
    ```

    - 您可以通过以下命令查看 Redis 状态

    ```shell
    sudo /etc/init.d/redis-server status
    ```

2. Redis 基本配置

    配置文件位于 `/etc/redis/redis.conf`

    > Redis 仅供本地软件使用，可以不单独开启外网访问与配置密码

# FA♂Q

~~还不知道写什么~~