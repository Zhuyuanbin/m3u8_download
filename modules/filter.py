#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  

def count_digits(number):
    # 将数字转换为字符串，然后计算字符串的长度
    num_str = str(number)
    num_digits = len(num_str)
    return num_digits

def can_convert_to_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def find_potential_ad_links(links):

    max_ts = len(links)
    valid_id_num = count_digits(max_ts)+1
    print(max_ts,valid_id_num)

    potential_ads = []  # 记录潜在的广告链接
    for link in links:
        file_name = link.split('/')[-1]  # 获取链接中的文件名部分
        print(file_name)
        file_id = file_name.split('.')[0]  # 提取文件编号
        print(f"文件编号：{file_id}")
        # 取文件id 后valid_id_num位转int
        last_digits = str(file_id)[-valid_id_num:]
        print(f"文件编号后{valid_id_num}位：{last_digits}")
        
        # 是否是正常以数值结尾的
        if not can_convert_to_int(last_digits):
            potential_ads.append(link)
            print(f"疑似广告链接：{link}")
            continue
        else:
            file_id_value = int(last_digits)
            if file_id_value >max_ts:
                potential_ads.append(link)
                print(f"疑似广告链接：{link}")
                continue             
    return potential_ads




if __name__ == "__main__":

    # 示例链接列表
    links = [
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001495.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001493.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001496.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001494.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001492.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001497.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001498.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65117129209641640.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65117129209641641.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65117129209641642.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65117129209641644.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001499.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65117129209641643.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001502.ts",
        "https://vip.ffzy-play7.com/20230112/11062_1c32df80/2000k/hls/65914b43fa1001500.ts"
    ]

    # 找出潜在的广告链接
    potential_ads = find_potential_ad_links(links)
    print("潜在的广告链接：")
    for link in potential_ads:
        print(link)
