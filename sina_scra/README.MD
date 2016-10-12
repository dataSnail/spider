一、运行爬虫需要做的工作
1、修改cmdline.py文件，运行指定爬虫
2、修改setting.py打开需要的pipeline配置（ITEM_PIPELINES）
3、修改setting.py修改LOG_FILE指定日志输出文件（linux和windows注意区别路径格式和读写权限）
4、修改middleware.py文件，修改代理地址
5、如果4修改了，注意修改setting.py文件中中间件的设置（DOWNLOADER_MIDDLEWARES）