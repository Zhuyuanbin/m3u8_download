#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  
import os,sys

from modules.searchMovie import MovieParse
from modules.download import Downloader,ThreadDownload
from modules.logger import logPrint
from modules.mergMp4 import merge_ts_namelist_to_mp4,merge_ts_to_mp4
from modules.downloadM3u8 import download_m3u8,parse_ts_urls
import time
import argparse
import shutil

from conf import config

class MovieDownloader:
    def __init__(self, movie_name):
        self.movie_name = movie_name
        self.base_url = "https://www.haituw.com"
        self.movie_parser = MovieParse(self.base_url,movie_name)

    def SearchMovie(self):
        response_html = self.movie_parser.SearchMove()
        self.movie_parser.ParaseHtml(response_html)
        movie_info = self.movie_parser.MatchMovieInfo()
        return movie_info
    
    def ParaseM3u8Url(self,movie_link):
        movie_source_link = self.movie_parser.GetNewHostApi(movie_link)
        
        m3u8sign_link = self.movie_parser.GetM3u8SignFromMovieSource(movie_source_link)
        m3u8_url = self.movie_parser.GetRealM3u8UrlFromM3u8Sign(m3u8sign_link)
        return m3u8_url
    







def MoveAndDel(movie_name):
    """
    3. 移动电影到指定目录了，如果目录不存在则不移动，存在则移动mp4,删除下载文件夹
    """
    if os.path.exists(config.MOVIE_TARGET_DIR):
        ts_dir = os.path.join(config.DOWNLOAD_MOVIE_BASE_DIR,movie_name)
        move_and_clean(ts_dir, config.MOVIE_TARGET_DI)


def move_and_clean(source_dir, target_dir):
    # 遍历目标目录中的所有文件和子目录
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 检查文件是否为MP4格式
            if not file.lower().endswith('.mp4'):
                file_path = os.path.join(root, file)
                # 删除非MP4格式的文件
                os.remove(file_path)
    # 移动源目录到目标目录
    shutil.move(source_dir, target_dir)
    logPrint(f"Moved {source_dir} to {target_dir}")




def GetM3u8FromMovieLink(movie_name,movie_link,movieDownloader= None):
    #从电影的url地址获取m3u8地址
    if movieDownloader == None:
        movieDownloader = MovieDownloader(movie_name)
    logPrint(f"开始解析<<{movie_name}>> {movie_link}的m3u8地址")
    m3u8_link = movieDownloader.ParaseM3u8Url(movie_link)
    logPrint(f"解析电影<<{movie_name}>>的m3u8地址成功：{m3u8_link}")
    return m3u8_link




def GetM3u8FromMovieName(movie_name):
    logPrint(f"开始搜索<<{movie_name}>>电影信息")
    movieDownloader = MovieDownloader(movie_name)
    movie_info = movieDownloader.SearchMovie()
    if movie_info:
        logPrint(f"电影搜索成功，信息数据如下：")
        print(f"""
                电影名:{movie_info['title']}
                链接:{movie_info['link']}
                年份:{movie_info['year']}
                资源:{movie_info['resource']}
                类型:{movie_info['tags']}
                导演:{movie_info['director']}
                主演:{movie_info['cast']}
            """)
    else:
        logPrint(f"未找到电影<<{movie_name}>> ")
        return None
    

    return GetM3u8FromMovieLink(movie_info['link'])





def AutoDownloadMovieFromName(movie_name):

    m3u8_link = GetM3u8FromMovieName(movie_name)
    if m3u8_link:
        download_ret = DownloadMovieFromM3u8(m3u8_link,movie_name)
        if download_ret:
            MoveAndDel()
        else:
            logPrint("电影下载失败")
    else:
        logPrint("解析电影失败")


def AutoDownloadMovieFromMovieLink(movie_link,movie_name):
    m3u8_link = GetM3u8FromMovieLink(movie_name,movie_link)
    if m3u8_link:
        download_ret = DownloadMovieFromM3u8(m3u8_link,movie_name)
        if download_ret:
            MoveAndDel()
        else:
            logPrint("电影下载失败")
    else:
        logPrint("解析电影失败")


def AutoDownloadMovieFromM3u8Link(m3u8_link,movie_name):
    download_ret = DownloadMovieFromM3u8(m3u8_link,movie_name)
    if download_ret:
        MoveAndDel()
    else:
        logPrint("电影下载失败")    




def DownloadMovieFromM3u8(m3u8_link,movie_name):
    logPrint(f"开始下载m3U8文件:{m3u8_link}")
    m3u8_content = download_m3u8(m3u8_link)
    if(m3u8_content == None):
        logPrint("下载m38u失败,请检查!")
        return
    logPrint("m3u8 文件下载成功!")

    logPrint("解析m3u8的base_url")
    m3u8_base_url = '/'.join(m3u8_link.split('/')[:-1]) + '/'  # 获取M3U8文件的基本URL
    logPrint(f"解析m3u8的base_url{m3u8_base_url}")

    logPrint("m3u8文件解析ts url")
    ts_urls = parse_ts_urls(m3u8_content, m3u8_base_url)
    logPrint(f"解析m3u8中含有{len(ts_urls)}个ts")


    ts_dir = os.path.join(config.DOWNLOAD_MOVIE_BASE_DIR,movie_name)
    failed_list_filename = "faild.txt"
    ThreadDownload(ts_urls,ts_dir)
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

        ThreadDownload(urls,ts_dir,failed_list_filename)
        retry_count+=1
        time.sleep(5)

    failed_file = os.path.join(ts_dir, failed_list_filename)
    if os.path.exists(failed_file):
        logPrint("存在ts文件重复下载失败,请手动查看")
        sys.exit()
    logPrint("ts文件准备完成!")

    logPrint("启动ffmpeg 合并ts文件")
    movie_full_name = os.path.join(ts_dir, movie_name)
    res = None
    if len(ts_urls)>=1024:
        res = merge_ts_namelist_to_mp4(ts_dir, movie_full_name)
    else:
        try:
            res = merge_ts_to_mp4(ts_dir, movie_full_name)
        except:
            res = merge_ts_namelist_to_mp4(ts_dir, movie_full_name)
    if res:
        logPrint(f"生成{movie_name} 成功")
        return True
    
    return False






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test m3u8 url download and parase ts url")
    parser.add_argument("-s", "--search", help="search movie name", required=False)
    parser.add_argument("-l", "--link", help="m3u8 or movieurl", required=False)
    args = parser.parse_args()
    


    movie_name = ''
    if args.search:
        movie_name = args.search
    else:
        movie_name = input("请输入下载的电影名称：")


    link = args.link
    if link:
        if link.endswith('.m3u8'):
            AutoDownloadMovieFromM3u8Link(link,movie_name)
        else:
            AutoDownloadMovieFromMovieLink(link,movie_name)
    else:
        AutoDownloadMovieFromName(movie_name)

    # 拆分3个步骤
    # 1. 根据输入（电影名称搜索，指定电影url） 得出真实的m3u8下载地址
    # 2. 根据m3u8下载地址，解析ts，多线程下载，合并成mp4
    # 3. 移动电影到指定目录了，如果目录不存在则不移动，存在则移动mp4,删除下载文件夹