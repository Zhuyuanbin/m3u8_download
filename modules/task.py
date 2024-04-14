import threading
import queue
import time

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modules.logger import logPrint
from modules.messageInfo import MovieDownLoadTask
from modules.app import AutoDownloadMovieFromM3u8Link,AutoDownloadMovieFromMovieLink,AutoDownloadMovieFromName
from conf import config
# 创建一个互斥锁
lock = threading.Lock()

# 任务队列
task_queue = queue.Queue()


def run():
    logPrint("task线程启动")
    while True:
        # 从队列中获取任务
        task = task_queue.get()
        logPrint(f"Consumed: {task}")
        
        try:
            movie_name = task.movie_name
            link = task.movie_link
            download_ret = False
            if link:
                if link.endswith('.m3u8'):
                    download_ret = AutoDownloadMovieFromM3u8Link(link,movie_name)
                else:
                    download_ret = AutoDownloadMovieFromMovieLink(link,movie_name)
            else:
                download_ret = AutoDownloadMovieFromName(movie_name)
            if download_ret:
                config.g_bot.send_message(config.admin_user, f"任务{task} 完成")
            else:
                config.g_bot.send_message(config.admin_user, f"任务{task} 失败")
        except:
            config.g_bot.send_message(config.admin_user, f"任务{task} 失败")
        # 任务处理完成，任务队列获取下一个任务
        task_queue.task_done()





task_thread1 = threading.Thread(target=run)



def AddMovieDownloadTask(task:MovieDownLoadTask):
    with lock:
        task_queue.put(task)
        logPrint(f"Add task: {task}")

