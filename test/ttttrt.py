import re

# 假设 html_data 是你的 HTML 数据
html_data = """
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,Chrome=1" />
    <meta http-equiv="X-UA-Compatible" content="IE=9" />
    <title>误杀2.HD国语版</title>
</head>
<link rel="stylesheet" type="text/css" href="/css/share.css">

<body onload="init()">

        <div class="gaog" id="gaog">
            <!--广告添加区域-->
            <div class="gaog-var">

            </div>
        </div>

        <div id="a1"></div>

        <div style="display:none" name="playtime" value="7131"></div>
        <div style="display:none" name="sizeview" value="1107681941"></div>
        <script type="text/javascript" src="/js/jquery-1.11.2.min.js" charset="utf-8"></script>
        <script type="text/javascript" src="/ckplayerx/ckplayer.js" charset="utf-8"></script>
                <link rel="stylesheet" href="/DPlayer/DPlayer.min.css">
<!--
<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<script src="https://cdn.jsdelivr.net/npm/dplayer@latest"></script>
-->
        <script src="/DPlayer/DPlayer.min.js"></script>
				<script src="/hls.min.js"></script>
		        <script src="/artplayer.js"></script>
        <script type="text/javascript">
            var video_player= 'artplayer'
            var tracker_url = ''
            var signaler_url = ''
            var auto_play = ''
            var hosts = '';
            var redirecturl = "http://vip.okzybo.com";
            var videoid = "ae0eb3eed39d2bcef4622b2499a05fe6";

            var id = 'ae0eb3eed39d2bcef4622b2499a05fe6'
            var     l = ''
            var     r= ''
            var     t= '15'
            var     d= ''
            var     u= ''

            var main = "/20221015/708_9b604134/index.m3u8?sign=a67617bfcc1414b3a6a557994cd6079b";
            var xml = "/20221015/708_9b604134/index.xml?sign=a67617bfcc1414b3a6a557994cd6079b";
            var pic = "/20221015/708_9b604134/1.jpg";
            var thumbnails = "/20221015/708_9b604134/thumbnails.jpg";
        </script>
        <script type="text/javascript" src="/js/share.js" charset="utf-8"></script>
        <script type="text/javascript">

        </script>

    <!--/广告添加区域-->
</body>

</html>
"""

# 使用正则表达式解析 var main 的值
pattern = r'var main = "(.*?)"'
match = re.search(pattern, html_data)

if match:
    main_value = match.group(1)
    print("var main 的值:", main_value)
else:
    print("未找到 var main 的值")


from urllib.parse import urlparse

# 假设 url 是你的 URL
url = "https://vip.ffzy-online.com/share/ae0eb3eed39d2bcef4622b2499a05fe6"


base_url = '/'.join(url.split('/')[:-1]) + '/'  # 获取M3U8文件的基本URL

print(base_url)




# 使用 urlparse 函数解析 URL
parsed_url = urlparse(url)


# 获取主机名和协议部分
hostname = parsed_url.netloc
scheme = parsed_url.scheme

print("协议:", scheme)
print("主机名:", hostname)