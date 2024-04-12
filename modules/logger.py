#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#

import logging
from logging import handlers

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import config


def log(log_path, stdout_type):
    """
    记录日志
    :param stdout_type:  输出到文件或console  eg: both: file and console; file: file; console: console
    :param log_path:  日志文件路径
    :return:
    """
    # 创建logger对象
    logger = logging.getLogger(log_path)
    # 清理上次用过的handler
    logger.handlers.clear()
    # 设置全局日志级别
    logger.setLevel(config.LOG_LEVEL)

    if stdout_type in ['file', 'both']:
        # 创建handler对象
        # file_handler = logging.FileHandler(log_file)
        # 带日志轮转的handler对象
        # 每天轮转一次，保留5个备份
        file_rotate_handler = handlers.TimedRotatingFileHandler(
            filename=log_path, encoding='utf8', when='D', interval=1, backupCount=50)

        # 生成formatter对象
        file_format = logging.Formatter(config.LOG_TO_FILE_FORMAT)

        # 给handler设置日志 级别
        # file_rotate_handler.setLevel('logging.{}'.format(level.upper()))

        # 把formatter对象绑定到handler对象
        file_rotate_handler.setFormatter(file_format)

        # 把handler对象绑定到logger对象
        logger.addHandler(file_rotate_handler)
        # logger.addFilter(IgnoreMsgFilter())

    if stdout_type in ['console', 'both']:
        # 输出到终端的handler
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter(config.LOG_TO_CONSOLE_FORMAT)
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger

cclog = log(config.APP_LOG_FILE, 'both')
logPrint = log(config.APP_LOG_FILE, 'both').info
# log('../test', 'both').info('this test message')
# log('../test', 'file').info('this test message')
# log('../test', 'console').info('this test message')

if __name__ == "__main__":
    logPrint("tttt")