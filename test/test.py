#!/usr/bin/env python3 
# -*- coding:utf-8 _*-
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from modules.searchMovie import SearchMove
from modules.paraseHtml import ParaseSearchHtml

import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test m3u8 url download and parase ts url")
    parser.add_argument("-s", "--search", help="search movie name", required=False)
    args = parser.parse_args()
    
    base_url = "https://www.haituw.com"

    movie_name = ''
    if args.search:
        movie_name = args.search
    else:
        movie_name = input("请输入下载的电影名称：")

    print(movie_name)
    response_res,session = SearchMove(base_url,movie_name)
    movies = ParaseSearchHtml(response_res)



    movie_info = {}

    for movie in movies:
        print(movie)
        if movie_name == movie['title']:
            """
            """
            movie_info = movie
            break
    if (not movie_info) and movies:
        movie_info = movies[0]

    if movie_info:
        print("电影名:", movie['title'])
        print("链接:", movie['link'])
        print("年份:", movie['year'])
        print("资源:", movie['resource'])
        print("类型:", movie['tags'])
        print("地区:", movie['area'])
        print("导演：", movie['director'])
        print("主演：", movie['cast'])
        print()
        if not movie['link'].startswith("/"):
            movie['link'] = "/" + movie['link']
        movie_url = base_url + movie['link']        


        print(f"获取{movie_name}电影 url成功：{movie_url}")
        print(f"{session.headers}")

    else:
        print(f"没有找到相关电影")
        

