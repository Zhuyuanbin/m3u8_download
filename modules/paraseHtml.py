#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  

from bs4 import BeautifulSoup
import re
html_doc = """
              <ul class="search-list">
                        <li class="item mb15 card-wrap">
                <div class="row">
                    <div class="img col-sm-2" style="">
                                                <a href="/movie/201-208831.html" class="thumb" target="_blank"><img src="/template/default/static/img/seize_img.jpg" class="lazy-load-img" _src="https://www.movieidc.com/upload/resource/201_208831_thumb.jpg"></a>
                                            </div>
                    <div class="txt col-sm-10">
                        <h5 class="subject ellipsis-one">
                                                        <a href="/movie/201-208831.html" target="_blank"><b><b style="color:red;">误杀2</b> <i class="fa fa-flag"></i></b></a>
                                                    </h5>
                        <p class="ellipsis-one year">年份：2021 </p>
                        <p class="area">地区：中国大陆 </p>
                        <p class="tags">类型：悬疑片</p>
                        <p class="ellipsis-one">导演：戴墨</p>
                        <p class="ellipsis-one">主演：肖央,任达华,文咏珊,陈雨锶,宋洋,李治廷,张世,尹子维,姜皓文,陈昊,周楚濋,王昊泽,强巴才丹</p>
                        <p>资源：HD国语版</p>
                        <p class="last">8个月前/3°C</em></p>
                    </div>
                </div>
            </li>
                        <li class="item mb15 card-wrap">
                <div class="row">
                    <div class="img col-sm-2" style="">
                                                <a href="/movie/201-281002.html" class="thumb" target="_blank"><img src="/template/default/static/img/seize_img.jpg" class="lazy-load-img" _src="https://www.movieidc.com/upload/resource/201_281002_thumb.jpg"></a>
                                            </div>
                    <div class="txt col-sm-10">
                        <h5 class="subject ellipsis-one">
                                                        <a href="/movie/201-281002.html" target="_blank"><b><b style="color:red;">误杀2</b> <i class="fa fa-flag"></i></b></a>
                                                    </h5>
                        <p class="ellipsis-one year">年份：2022 </p>
                        <p class="area">地区：中国大陆 </p>
                        <p class="tags">类型：犯罪片</p>
                        <p class="ellipsis-one">导演：不详</p>
                        <p class="ellipsis-one">主演：肖央,谭卓,陈冲,姜皓文</p>
                        <p>资源：正片</p>
                        <p class="last">2023-03-23 22:04:39/0°C</em></p>
                    </div>
                </div>
            </li>
                        <li class="item mb15 card-wrap">
                <div class="row">
                    <div class="img col-sm-2" style="">
                                                <a href="/movie/201-236745.html" class="thumb" target="_blank"><img src="/template/default/static/img/seize_img.jpg" class="lazy-load-img" _src="https://www.movieidc.com/upload/resource/201_236745_thumb.jpg"></a>
                                            </div>
                    <div class="txt col-sm-10">
                        <h5 class="subject ellipsis-one">
                                                        <a href="/movie/201-236745.html" target="_blank"><b><b style="color:red;">误杀2</b>优酷独家幕后记录 <i class="fa fa-flag"></i></b></a>
                                                    </h5>
                        <p class="ellipsis-one year">年份：2021 </p>
                        <p class="area">地区：中国大陆 </p>
                        <p class="tags">类型：纪录片</p>
                        <p class="ellipsis-one">导演：戴墨</p>
                        <p class="ellipsis-one">主演：肖央,任达华,文咏珊,陈雨锶,宋洋,李治廷,张世,尹子维,姜皓文,陈昊,周楚濋,王昊泽,强巴才丹</p>
                        <p>资源：正片</p>
                        <p class="last">2023-03-21 01:58:01/0°C</em></p>
                    </div>
                </div>
            </li>
                        <li class="item mb15 card-wrap">
                <div class="row">
                    <div class="img col-sm-2" style="">
                                                <a href="/movie/201-285902.html" class="thumb" target="_blank"><img src="/template/default/static/img/seize_img.jpg" class="lazy-load-img" _src="https://www.movieidc.com/upload/resource/201_285902_thumb.jpg"></a>
                                            </div>
                    <div class="txt col-sm-10">
                        <h5 class="subject ellipsis-one">
                                                        <a href="/movie/201-285902.html" target="_blank"><b><b style="color:red;">误杀2</b> 独家幕后记录 <i class="fa fa-flag"></i></b></a>
                                                    </h5>
                        <p class="ellipsis-one year">年份：2021 </p>
                        <p class="area">地区：中国大陆 </p>
                        <p class="tags">类型：纪录片</p>
                        <p class="ellipsis-one">导演：戴墨</p>
                        <p class="ellipsis-one">主演：肖央,任达华,文咏珊,陈雨锶,宋洋,李治廷,张世,尹子维,姜皓文,陈昊,周楚濋,王昊泽,强巴才丹</p>
                        <p>资源：正片</p>
                        <p class="last">2022-12-24 11:42:12/0°C</em></p>
                    </div>
                </div>
            </li>
                    </ul>

"""










def ParaseSearchHtml(html_res):
    soup = BeautifulSoup(html_doc, 'html.parser')

    movies = []
    for li in soup.find_all('li', class_='item mb15 card-wrap'):
        movie = {}
        movie_title = li.find('h5', class_='subject ellipsis-one')
        if movie_title:
            movie['title'] = movie_title.text.strip()
        else:
            movie['title'] = "Unknown"
        movie_link = li.find('a', href=True)
        if movie_link:
            movie['link'] = movie_link['href']
        else:
            movie['link'] = "Unknown"
        movie_year = li.find('p', class_='year')
        if movie_year:
            movie['year'] = movie_year.text.strip().split('：')[1]
        else:
            movie['year'] = "Unknown"

        movie_area = li.find('p', class_='area')
        if movie_area:
            movie['area'] = movie_area.text.strip().split('：')[1]
        else:
            movie['area'] = "Unknown"

        movie_tags = li.find('p', class_='tags')
        if movie_tags:
            movie['tags'] = movie_tags.text.strip().split('：')[1]
        else:
            movie['tags'] = "Unknown"

        director_tag = li.find('p', text=lambda text: text and "导演：" in text)
        movie['director'] = director_tag.text.strip().split('：')[1] if director_tag else "Unknown"

        cast_tag = li.find('p', text=lambda text: text and "主演：" in text)
        movie['cast'] = cast_tag.text.strip().split('：')[1] if cast_tag else "Unknown"

        movie_resource_tag = li.find('p', text=lambda text: text and "资源：" in text)
        if movie_resource_tag:
            next_p_tag = movie_resource_tag.find_next_sibling('p')
            if next_p_tag and next_p_tag.find('a'):
                movie['resource'] = next_p_tag.text.strip()
            else:
                movie['resource'] = movie_resource_tag.text.strip().split('：')[1]
        else:
            movie['resource'] = "Unknown"

        movies.append(movie)
    return movies







if __name__ == "__main__":
    movies = ParaseSearchHtml(html_doc)
    for movie in movies:
        print("电影名:", movie['title'])
        print("链接:", movie['link'])
        print("年份:", movie['year'])
        print("资源:", movie['resource'])
        print("类型:", movie['tags'])
        print("地区:", movie['area'])
        print("导演：", movie['director'])
        print("主演：", movie['cast'])
        print()
