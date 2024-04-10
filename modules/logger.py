#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  

import logging
from datetime import datetime

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")
# 设置日志文件名
log_file = f'm3u8_download_{current_date}.log'
# 设置日志格式
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def logPrint(msg,type =2):
    if(type ==2):
        print(msg)
        logging.info(msg)
    else:
        print(msg)


if __name__ == "__main__":
    logPrint("Test Test")