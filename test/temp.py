    with open('index.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        downloader.add_url(url)
