一、运行爬虫需要做的工作
1、修改cmdline.py文件，运行指定爬虫
2、修改setting.py打开需要的pipeline配置（ITEM_PIPELINES）
3、修改setting.py修改LOG_FILE指定日志输出文件（linux和windows注意区别路径格式和读写权限）
4、修改middleware.py文件，修改代理地址
5、如果4修改了，注意修改setting.py文件中中间件的设置（DOWNLOADER_MIDDLEWARES）


多爬虫运行脚本：（与爬虫放在同一目录下）

#!/bin/bash
echo "Please input the spide numbers"
read data
for((i=0; i<$data; i++));
do
    sudo cp -R /usr/local/src/spider /usr/local/src/spider_$i
#echo $data
done
echo "Run the spiders(spider_0~~spider_$[data-1]) right now?(y/n)"
read isnow
if [ "$isnow"x = "y"x ];
then
for ((j=0; j<$data; j++));
do
    cd /usr/local/src/spider_$j
    # log file path /usr/local/src/logs/
    sudo scrapy crawl user_relation -s LOG_FILE=/usr/local/src/logs/spider_${j}.log&
    echo "spider_$j is RUNNING..."
done
else
   echo "spider is NOT running..."
fi

