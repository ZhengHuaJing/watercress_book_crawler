### 这是什么鬼？
这是一个爬取豆瓣所有标签下图书的爬虫，运行后会根据规矩不断爬取图书直到结束，会将爬取到的数据写入到 MongoDB 数据库


### 要用到什么？
1. 安装 scrapy 框架    

- Windows 安装方式
    - Python 2 / 3
    - 升级pip版本：pip install --upgrade pip
    - 通过pip 安装 Scrapy 框架pip install Scrapy

- Ubuntu 需要9.10或以上版本安装方式
    - Python 2 / 3
    - 安装非Python的依赖 sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
    - 通过pip 安装 Scrapy 框架 sudo pip install scrapy

- 安装后，只要在命令终端输入 scrapy，提示类似以下结果，代表已经安装成功
![输入图片说明](https://gitee.com/uploads/images/2018/0215/161648_81674a17_1577043.png "7.1.png")

2. 安装 MongoDB 数据库
- Windows 平台安装 MongoDB
http://www.runoob.com/mongodb/mongodb-window-install.html

- Linux平台安装MongoDB
http://www.runoob.com/mongodb/mongodb-linux-install.html

- Mac OSX 平台安装 MongoDB
http://www.runoob.com/mongodb/mongodb-osx-install.html


### 怎么配置呀？
1. 豆瓣账号和密码设置

打开 watercress_book_crawler/doubanbook/spiders/dbb.py 文件，将其中的 username 改为豆瓣账号，password 改为豆瓣密码（单引号别丢了)

![输入图片说明](https://gitee.com/uploads/images/2018/0215/155754_59d53e99_1577043.jpeg "1518681332683.jpg")

2. MongoDB 数据库配置
打开 watercress_book_crawler/doubanbook/settings.py 文件，设置对应的字段值（默认的话不用更改）

![输入图片说明](https://gitee.com/uploads/images/2018/0215/163333_afc5ffc9_1577043.png "WX20180215-163315.png")

### 项目怎么用？
1. 下载项目
   
git clone https://gitee.com/cix/watercress_book_crawler.git

2. 进入项目文件夹

cd watercress_book_crawler/

3. 执行项目

scrapy crawl dbb

### 最后的结果？
- 保存的字段

![输入图片说明](https://gitee.com/uploads/images/2018/0215/163757_627b4b4f_1577043.png "WX20180215-163735.png")

- 数据库

![输入图片说明](https://gitee.com/uploads/images/2018/0215/163901_40104a00_1577043.jpeg "1518683824526.jpg")

