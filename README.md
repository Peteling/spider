# spider
爬取steam游戏,maoyan电影,amazon图书
## steam
### steam爬取过程的问题
1. 部分页面会重定向到验证页面，例如年龄验证，生日验证，未成年等等各种验证
解决方法：捕捉验证之后的cookie，抓取时存入Request即可
2. 游戏发布日期的处理
很多游戏的发布日期格式不一样，数据处理的时候比较麻烦，着重分别处理了 年月日,年月,年这三种格式，其他不处理
3. 爬取了前500页的游戏资讯，因为在后面页码中很多不是游戏
4. 数据库存储采用mongodb，不能映射python的date格式，所以日期基本是原样存入
5. spider继承scrapy的基本类spider
## Amazon
### 爬取亚马逊图书过程的问题
1. spider继承scrapy的CrawlSpider（只用来索引下一页的链接）
2. 数据库存储采用mysql

## film
### 爬取猫眼电影资讯的问题
1. http://maoyan.com/films 猫眼电影这个网站防爬虫机制比较严格，很难一次抓取所有信息，爬取一定量电影后网站会识别到爬虫并重定向到验证码页面（至今没解决）

## requirements
1. scrapy>=1.1.1
2. scrapy-fake-useragent 产生动态的 User-Agent
3. scrapy-proxies 配置后可以使用 IP 代理

## settings
```python
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_IP = 16
```
