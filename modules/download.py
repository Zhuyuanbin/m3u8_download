#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  
import threading
import queue
import requests
import argparse
import time
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modules.logger import logPrint
from modules.mergMp4 import merge_ts_namelist_to_mp4,merge_ts_to_mp4
from modules.downloadM3u8 import download_m3u8,parse_ts_urls


class Downloader:
    def __init__(self, output_dir, urls_file, max_retry=3):
        self.download_queue = queue.Queue()
        self.failed_urls = []
        self.max_retry = max_retry
        self.completed_count = 0
        self.total_count = 0
        self.output_dir = output_dir
        self.urls_file = urls_file
        self.start_time = 0
        self.end_time = 0
        self.status = 0

        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)



    def add_url(self, url):
        self.download_queue.put(url)
        self.total_count += 1

    def download_file(self, url):
        retry_count = 0
        while retry_count < self.max_retry:
            try:
                response = requests.get(url,timeout=180)
                if response.status_code == 200:
                    filename = os.path.join(self.output_dir, url.split('/')[-1])
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                        self.completed_count += 1

                        
                    print(f"Downloaded {url} ({self.completed_count}/{self.total_count})")
                    return
                else:
                    logPrint(f"Failed to download {url}. Status code: {response.status_code}")
            except Exception as e:
                logPrint(f"Exception occurred while downloading {url}: {e}")
            retry_count += 1
        self.failed_urls.append(url)
        logPrint(f"Failed to download {url} after {self.max_retry} retries")

    def download_manager(self):
        while True:
            url = self.download_queue.get()
            try:
                self.download_file(url)
            except:
                logPrint(f"Failed to download {url}  except")
            self.download_queue.task_done()

    def start_downloader(self, num_workers=4):
        self.status = 1
        self.start_time = time.time()

        for _ in range(num_workers):
            worker = threading.Thread(target=self.download_manager)
            worker.daemon = True
            worker.start()

        self.download_queue.join()

        self.end_time = time.time()
        
        print("All downloads completed.")
        if self.failed_urls:
            print("Failed URLs:")
            for url in self.failed_urls:
                print(url)
            # 将失败的 URL 写入文件
            failed_file = os.path.join(self.output_dir, self.urls_file)
            with open(failed_file, "w") as f:
                for url in self.failed_urls:
                    f.write(url + "\n")
            logPrint(f"Failed URLs written to: {failed_file}")
        self.status = 0
        logPrint(f"Completed: {self.completed_count}, Total: {self.total_count}")
        logPrint(f"Total time taken: {self.end_time - self.start_time} seconds")




def ThreadDownload(ts_urls,ts_dir,failed_list_filename='faild.txt',num_workers=16):
    logPrint("初始化多线程下载...")
    # 2. 多线程下载ts文件，下载出错的ts文件 写入failed.txt文件列表
    downloader = Downloader(output_dir=ts_dir, urls_file=failed_list_filename)
    for url in ts_urls:
        downloader.add_url(url)

    logPrint(f"启动{num_workers}个线程开始下载...")
    # Start downloader with 2 worker threads
    downloader.start_downloader(num_workers)

    while(downloader.status):
        time.sleep(0.5)

    logPrint(f"多线程下载完成")


# python .\download.py -n test.mp4 -o ./test/ -l https://vip.ffzy-play.com/20221218/37532_a7d57d68/2000k/hls/index.m3u8
#https://vip.ffzy-play.com/20221218/37532_a7d57d68/2000k/hls/index.m3u8
if __name__ == "__main__":
    # 1. 输入m3u8的url链接，指定输出目录，输出文件名，下载解析出ts的url
    # 2. 多线程下载ts文件，下载出错的ts文件 写入failed.txt文件列表
    # 3. 循环3次 检查是否有failed.txt文件,有=>读取failed.txt文件并删除,启动文件下载, sleep 10s
    # 4. 调用ffmpeg进行合并ts
    parser = argparse.ArgumentParser(description="Downloader with multiple threads")
    parser.add_argument("-o", "--output", help="Output directory for downloaded files", required=True)
    parser.add_argument("-n", "--name", help="merg ts to movie name", required=True)
    parser.add_argument("-fl", "--failedlist", help="File containing URLs to download", required=False)
    parser.add_argument("-t", "--thread", help="set thread count", required=False)
    parser.add_argument("-l", "--link", help="m3u8 url link", required=True)
    args = parser.parse_args()


    logPrint("初始化参数...")
    # 1. 输入m3u8的url链接，指定输出目录，输出文件名，下载解析出ts的url
    m3u8_link = args.link
    ts_dir = args.output
    movie_name = args.name
    failed_list_filename = "faild.txt"
    if args.failedlist:
        failed_list_filename = args.failedlist

    num_workers = 16
    if args.thread:
        num_workers = args.thread



    log_message = ""

    log_message = f"m3u8 link :{m3u8_link};  ts_dir:{ts_dir};  movie name:{movie_name};  faild_list:{failed_list_filename};  num_workers:{num_workers}"
    logPrint(log_message)

    logPrint("下载m3u8文件..")
    m3u8_content = download_m3u8(args.link)
    if(m3u8_content == None):
        logPrint("下载m38u失败,请检查!")
        sys.exit()

    logPrint("m3u8 文件下载成功!")

    logPrint("解析base_url")
    base_url = '/'.join(m3u8_link.split('/')[:-1]) + '/'  # 获取M3U8文件的基本URL

    logPrint(f"base_url={base_url}")


    logPrint("m3u8文件解析ts url")
    ts_urls = parse_ts_urls(m3u8_content, base_url)
    logPrint(f"解析m3u8中含有{len(ts_urls)}个ts")



    ThreadDownload(ts_urls,ts_dir,failed_list_filename,num_workers)


    # 3. 循环3次 检查是否有failed.txt文件,有=>读取failed.txt文件并删除,启动文件下载, sleep 10s
    retry_count = 0
    while retry_count <3:
        logPrint("检测是否有失败列表")
        failed_file = os.path.join(ts_dir, failed_list_filename)
        if not os.path.exists(failed_file):
            logPrint("全部下载完成,不存在失败列表")
            break

        urls = []
        with open(failed_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]

        os.remove(failed_file)

        ThreadDownload(urls,ts_dir,failed_list_filename,num_workers)
        retry_count+=1
        time.sleep(5)

    failed_file = os.path.join(ts_dir, failed_list_filename)
    if os.path.exists(failed_file):
        logPrint("存在ts文件重复下载失败,请手动查看")
        sys.exit()
    logPrint("ts文件准备完成!")

    """
    logPrint("开始生成ffmpeg读取文件列表")
    ts_files_list = parse_ts_urls(m3u8_content,'')
    logPrint(f"读取到{len(ts_files_list)}个ts文件")
    ts_files_fullname= os.path.join(ts_dir, "nameList.txt")
    with open(ts_files_fullname, "w") as f:
        for file_name in ts_files_list:
            f.write("file '{}'\n".format(file_name))
    
    logPrint("生成{ts_files_fullname}文件列表成功")
    """


    logPrint("启动ffmpeg 合并ts文件")
    movie_full_name = os.path.join(ts_dir, movie_name)
    res = None
    if len(ts_urls)>=1024:
        res = merge_ts_namelist_to_mp4(ts_dir, movie_full_name)
    else:
        res = merge_ts_to_mp4(ts_dir, movie_full_name)
    if res:
        logPrint(f"生成{movie_name} 成功")




