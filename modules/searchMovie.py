#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  

"""
获取电影的搜索结果
"""

from urllib.parse import quote,urlparse,urljoin
import requests
import time
import argparse
import re
import json

from .logger import logPrint
from .paraseHtml import ParaseSearchHtml




class MovieParse:
    def __init__(self, base_url, movie_name):
        self.base_url = base_url
        self.movie_name = movie_name
        self.session = None
        self.movies = []
        self.movie_info = {}
        self.SessionInit()


    def SessionInit(self):
        if self.session == None:
            # 初始化session
            url = self.base_url+"/search/"+ quote(self.movie_name)

            # Session object to persist cookies
            self.session = requests.Session()

            # Send the first request to get cookies
            response = self.session.get(url)

            # Check if the request was successful
            if response.ok:
                logPrint("电影解析器初始化成功...")
                return True
            else:
                logPrint("初始化失败")
                self.session = None
                return False
        return True




    def MatchMovieInfo(self):
        self.movie_info = self.MatchMovieInfoEx(self.movies)
        return self.movie_info

    def MatchMovieInfoEx(self,movies):
        movie_info = {}
        for movie in movies:
            print(movie)
            if self.movie_name == movie['title']:
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
            movie['link'] = self.base_url + movie['link']        
            print(f"获取{self.movie_name}电影 url成功：{movie['link']}")
        else:
            print(f"没有找到相关电影")
        return movie_info


    def ParaseHtml(self,html_doc):
        self.movies = ParaseSearchHtml(html_doc)
        return self.movies


    def SearchMove(self):
        return self.SearchMoveEx(self.base_url,self.movie_name)

    def SearchMoveEx(self,base_url,movie_name):

        session_init_ret = self.SessionInit()
        url = base_url+"/search/"+ quote(movie_name)
        # Check if the request was successful
        if session_init_ret:
            print("First request successful.")
            time.sleep(4)
            # Send the second request with cookies attached to headers
            #response = self.session.get(url, headers={'Cookie': '; '.join([f"{k}={v}" for k, v in cookies.items()])})
            response = self.session.get(url)
            # print(self.session.headers)
            # Check if the second request was successful
            if response.ok:
                print("Second request successful.")
                # Print the response content
                print("Response content:", response.text)
                return response.text
                print("Second request failed.")
        else:
            print("First request failed.")
        return None



    def GetNewHostApi(self, movie_url):
        """
        获取电影源站
        """

        self.SessionInit()
        post_data_dict = {
            'order': 'getNewHost',
            'aid': '',
            'sid': '',
            'mid': '',
            'isstatic': '1',
            'target': 'movieDetails',
            'rp0': '0',
            'rp1': '0',
            'isBackServerRsData': '1'
        }


        #post_data_str_back = urlencode(post_data_dict, doseq=False)

        movie_html = movie_url.split('/')[-1]
        sid_mid = movie_html.split('.')[0]
        post_data_dict['sid'] = sid_mid.split('-')[0]
        post_data_dict['mid'] = sid_mid.split('-')[1]

        interface_url = self.base_url+"/common/api_getNewHost.php"

        # 定义 Referer 头
        referer_header = {
            'Referer': movie_url+f"&play={post_data_dict['rp0']}-{post_data_dict['rp1']}"
        }

        # 合并请求头
        headers = {**referer_header}



        response = self.session.post(interface_url,post_data_dict, headers=headers)


        # 检查请求是否成功
        if response.ok:
            print("POST 请求成功")
            # 如果响应的内容是 JSON 格式，则解析 JSON 数据
            if 'application/json' in response.headers.get('content-type', ''):
                json_data = json.loads(response.content.decode('utf-8-sig'))
                print("解析后的 JSON 数据:", json_data)
                return json_data['data']['url']
            else:
                print("响应内容不是 JSON 格式")
                print("响应内容:", response.text)
        else:
            print("POST 请求失败")


    def GetM3u8SignFromMovieSource(self,movie_source_link):
        """
        在电影源站，获取m3u8签名地址
        """
        session = requests.Session()
        response = self.session.get(movie_source_link)
        # print(self.session.headers)
        # Check if the second request was successful
        if response.ok:
            print("Second request successful.")
            # Print the response content
            print("Response content:", response.text)
            # 使用正则表达式解析 var main 的值
            pattern = r'var main = "(.*?)"'
            match = re.search(pattern, response.text)

            if match:
                main_value = match.group(1)
                print("var main 的值:", main_value)


                # 使用 urlparse 函数解析 URL
                parsed_url = urlparse(movie_source_link)
                # 获取主机名和协议部分
                hostname = parsed_url.netloc
                scheme = parsed_url.scheme
                m3u8_base_url = scheme+"://"+hostname


                if not main_value.startswith("/"):
                    main_value = "/" + main_value
                main_value = m3u8_base_url + main_value   
                return main_value
            else:
                print("未找到 var main 的值")
            
        else:
            return None
        return None


    def GetRealM3u8UrlFromM3u8Sign(self,m3u8_sign_url):
        """
        根据m3u8签名地址 获解析m3u8地址
        """
        response = requests.get(m3u8_sign_url)
        if response.status_code == 200:
            m3u8_content = response.text
            # 使用 urlparse 函数解析 URL


            m3u8_base_url = '/'.join(m3u8_sign_url.split('/')[:-1]) + '/'  # 获取M3U8文件的基本URL
            ts_urls = [line.strip() for line in m3u8_content.split('\n') if line.strip().endswith('.ts')]
            m3u8_urls = [urljoin(m3u8_base_url, line.strip()) for line in m3u8_content.split('\n') if line.strip().endswith('.m3u8')]
            if len(ts_urls)>10 and not m3u8_urls:
                return m3u8_sign_url
            elif m3u8_urls:
                return m3u8_urls[0]
            else:
                print("解析m3u8失败")
        else:
            print(f"打开M3u8Sign地址失败 {m3u8_sign_url}")


        return None




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


    movie_parser = MovieParse(base_url,movie_name)
    response_html = movie_parser.SearchMove()
    movie_parser.ParaseHtml(response_html)
    movie_info = movie_parser.MatchMovieInfo()
    
    
    # 返回的电影源链接,https://vip.ffzy-online.com/share/ae0eb3eed39d2bcef4622b2499a05fe6
    movie_source_link = movie_parser.GetNewHostApi(movie_info['link'])
    
    m3u8sign_link = movie_parser.GetM3u8SignFromMovieSource(movie_source_link)
    print(m3u8sign_link)

    m3u8_url = movie_parser.GetRealM3u8UrlFromM3u8Sign(m3u8sign_link)

    print(f"获取的m3u8url:{m3u8_url}")
