#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  
""" 

"""


import logging
# import telegram
# 将当前目录添加到Python搜索路径中
import os,sys
# 工作目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOWNLOAD_MOVIE_BASE_DIR = os.path.join(BASE_DIR, 'download')

MOVIE_TARGET_DIR = "/volume1/share/media/movie/"

# 日志目录
LOG_PATH = os.path.join(BASE_DIR, 'logs')

# 程序日志文件路径
APP_LOG_FILE = os.path.join(LOG_PATH, 'app.log')

# 日志级别 DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = logging.INFO

# 日志格式
# 写入文件格式
LOG_TO_FILE_FORMAT = '[%(asctime)s] [%(levelname)s] %(filename)s:%(funcName)s:%(lineno)s - %(message)s'
# 写入console格式
LOG_TO_CONSOLE_FORMAT = '%(message)s'

# 创建相关目录
if not os.path.isdir(LOG_PATH): os.makedirs(LOG_PATH, exist_ok=True)
if not os.path.isdir(DOWNLOAD_MOVIE_BASE_DIR): os.makedirs(DOWNLOAD_MOVIE_BASE_DIR, exist_ok=True)



bot_token = "998665615:AAHv5PcGOkFujOQBVKOHnFvBvnOoDvvG-0A"

# g_bot = telegram.Bot(bot_token)
