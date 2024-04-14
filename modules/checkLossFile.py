
import argparse
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from modules.logger import logPrint
from modules.downloadM3u8 import download_m3u8,parse_ts_urls






def find_missing_files(file_list, target_directory):
    # 获取目标目录中的文件列表
    target_files = os.listdir(target_directory)
    
    # 找到不在目标目录中的文件名
    missing_files = []
    for file_name in file_list:
        if file_name not in target_files:
            missing_files.append(file_name)
    
    return missing_files





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Downloader with multiple threads")
    parser.add_argument("-o", "--output", help="Output directory for downloaded files", required=True)
    parser.add_argument("-l", "--link", help="m3u8 url link", required=True)
    args = parser.parse_args()

    m3u8_content = download_m3u8(args.link)
    ts_urls = parse_ts_urls(m3u8_content, '')

    missing_files = find_missing_files(ts_urls, args.output)
    print("不在目标目录中的文件名：", missing_files)
