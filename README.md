## 增强版Python爬虫+WordPress
与之前完成的单站点爬虫测试相比，现在通过从数据库读取爬取规则，做了多站点适配
而且爬虫的部署比以前更加简单。
站点配置在example文件夹数据库有示例

### 配置爬虫

#### 修改配置文件wp.conf
    1.增加数据库配置
    2.增加WordPress站点配置
    站点信息请加上xmlrpc.php
    ```
    website=http://itfin.jj.cn/xmlrpc.php
    ```
    3.增加email配置

#### 创建数据库
     ```
     python3  manage.py createDB
     ```
#### 增加站点
      在数据库里增加要爬取的站点配置信息
      **站点配置信息一定要准确，不然爬不到数据**
      ```
      python3 manage.py addConf
      ```
      限制爬虫的站点暂时不可爬

#### 运行爬虫

    ```
    python3 wpspider.py
    ```
