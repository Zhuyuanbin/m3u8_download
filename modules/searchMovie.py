#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  

"""
获取电影的搜索结果
"""



from urllib.parse import quote
import requests
import time

def SearchMove(base_url,movie_name):
    #base_url = "https://www.haituw.com"
    url = base_url+"/search/"+ quote(movie_name)

    # Session object to persist cookies
    session = requests.Session()

    # Send the first request to get cookies
    response = session.get(url)

    # Check if the request was successful
    if response.ok:
        print("First request successful.")
        # Get cookies from the response
        cookies = session.cookies.get_dict()
        print("Cookies:", cookies)
        time.sleep(4)
        # Send the second request with cookies attached to headers
        response = session.get(url, headers={'Cookie': '; '.join([f"{k}={v}" for k, v in cookies.items()])})

        # Check if the second request was successful
        if response.ok:
            print("Second request successful.")
            # Print the response content
            print("Response content:", response.text)
            return response.text
        else:
            print("Second request failed.")
    else:
        print("First request failed.")


if __name__ == "__main__":
    base_url = "https://www.haituw.com"
    #SearchMove(base_url,"误杀2")