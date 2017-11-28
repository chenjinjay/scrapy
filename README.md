一、my_spider/my_spider/spiders/dmoz.py: 入门练习时创建的项目，可参考：https://zhuanlan.zhihu.com/p/24669128

二、my_spider/my_spider/spiders/douban_spider.py: 框架使用练习项目，豆瓣电影爬虫，可参考：http://woodenrobot.me/2017/01/07/Scrapy%E7%88%AC%E8%99%AB%E6%A1%86%E6%9E%B6%E6%95%99%E7%A8%8B%EF%BC%88%E4%BA%8C%EF%BC%89-%E7%88%AC%E5%8F%96%E8%B1%86%E7%93%A3%E7%94%B5%E5%BD%B1TOP250/

三、2017-11-27增加了将数据插入到数据库的模块pipline.py
(1)源码参考：
https://github.com/lawlite19/PythonCrawler-Scrapy-Mysql-File-Template/blob/master/webCrawler_scrapy/pipelines.py  为了不让数据插入库后有重复的现在，比源码增加了 import copy的一步，具体看本项目里面的pipelines.py
(2)教程参考：
http://blog.csdn.net/u013082989/article/details/52589791
四、解决spider爬取数据正常，但是插入mysql时发生数据重复（前面或者后面的数据被覆盖）
下面来自cdsn的评论，源链接如下：http://bbs.csdn.net/topics/391847368   用户：qq_33245827 的评论：

其原因是由于Spider的速率比较快，而scapy操作数据库操作比较慢，导致pipeline中的方法调用较慢，这样当一个变量正在处理的时候，一个新的变量过来，之前的变量的值就会被覆盖，比如pipline的速率是1TPS，而spider的速率是5TPS，那么数据库应该会有5条重复数据。

解决方案是对变量进行保存，在保存的变量进行操作，通过互斥确保变量不被修改
    #pipeline默认调用
    def process_item(self, item, spider):
        #深拷贝
        asynItem = copy.deepcopy(item)
        d = self.dbpool.runInteraction(self._do_upinsert, asynItem, spider)
