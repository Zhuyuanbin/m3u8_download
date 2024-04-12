from urllib.parse import parse_qs, urlencode

# 定义 POST 数据字符串
post_data_str = "order=getNewHost&aid=&sid=201&mid=208831&isstatic=1&target=movieDetails&rp0=0&rp1=0&isBackServerRsData=1"

# 将 POST 数据字符串解析为字典
post_data_dict = parse_qs(post_data_str)

print("解析后的字典:", post_data_dict)

# 定义要转换回字符串的字典
post_data_dict_back = {
    'order': 'getNewHost',
    'aid': '',
    'sid': '201',
    'mid': '208831',
    'isstatic': '1',
    'target': 'movieDetails',
    'rp0': '0',
    'rp1': '0',
    'isBackServerRsData': '1'
}

# 将字典编码为 POST 数据字符串
post_data_str_back = urlencode(post_data_dict_back, doseq=False)

print("转换后的字符串:", post_data_str_back)
