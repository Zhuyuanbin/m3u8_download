import requests
from urllib.parse import urljoin

def download_m3u8(url):
    # 发送请求获取M3U8文件内容
    response = requests.get(url)
    if response.status_code == 200:
        m3u8_content = response.text
        return m3u8_content
    else:
        print("Failed to download M3U8 file")
        return None

def parse_ts_urls(m3u8_content, base_url):
    # 使用正则表达式解析TS文件URL
    ts_urls = [urljoin(base_url, line.strip()) for line in m3u8_content.split('\n') if line.strip().endswith('.ts')]
    return ts_urls

def main():
    m3u8_url = input("请输入M3U8文件的URL：")
    base_url = '/'.join(m3u8_url.split('/')[:-1]) + '/'  # 获取M3U8文件的基本URL
    
    # 下载M3U8文件内容
    m3u8_content = download_m3u8(m3u8_url)
    if m3u8_content:
        # 解析TS文件URL
        ts_urls = parse_ts_urls(m3u8_content, base_url)
        
        # 打印所有TS文件URL
        print("解析到的TS文件URL：")
        for url in ts_urls:
            print(url)

if __name__ == "__main__":
    main()
