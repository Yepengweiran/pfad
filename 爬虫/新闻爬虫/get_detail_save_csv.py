import sys
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class request:
    def get_html_text(self, url, params=None, headers=None):
        try:
            response = requests.get(url, params=params, headers=headers)
            response.encoding = 'utf-8'
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return None

    def parse_html(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup

    def get_html_json(self, url, params, headers):
        try:
            response = requests.get(url, params=params, headers=headers)
            response.encoding = 'utf-8'
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return None

repr = request()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.chinanews.com.cn",
    "Sec-Ch-Ua": '"Microsoft Edge";v="123", "Not\\A-Brand";v="8", "Chromium";v="123"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
}

# 读取news_url文件夹下的所有txt文件
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'news_url')
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# 定义CSV文件的头
csv_headers = ['title', 'content', 'publish_time', 'source', 'image_urls', 'detail_url']
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'news_data.csv')

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_headers)

    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            urls = file.readlines()

        for url in urls:
            url = url.strip()
            print(f"正在抓取：{url}")
            html_doc = repr.get_html_text(url=url, headers=headers)
            if html_doc:
                soup = repr.parse_html(html_doc)

                # 正文
                paragraphs = soup.find_all('p')
                text1 = ''
                for p in paragraphs:
                    text1 += p.text
                    if p.text.endswith('(完)'):
                        break

                # 标题
                title = soup.find('title').text

                # 时间和来源
                time_div = soup.find('div', class_='content_left_time')
                if time_div:
                    time_text = time_div.text.strip()
                    time_and_source = time_text.split('\n\n\n')[0]
                    parts = time_and_source.split('来源：')
                    if len(parts) >= 2:
                        time = parts[0].strip()
                        source = '来源：' + parts[1].strip()
                    else:
                        print("Time and source information not properly formatted.")
                        time = ''
                        source = ''
                else:
                    print("Time and source information not found.")
                    time = ''
                    source = ''

                # 图片
                img_tags = soup.find_all('img')
                img_urls = []
                for img_tag in img_tags:
                    if img_tag.get('style') == "display: block; margin: auto; cursor: pointer;":
                        img_src = img_tag.get('src')
                        if img_src and img_src.startswith('//'):
                            img_src = 'https:' + img_src
                            img_urls.append(img_src)

                image_urls_str = ','.join(img_urls)

                try:
                    publish_time_obj = datetime.strptime(time, '%Y年%m月%d日 %H:%M')
                    publish_time = publish_time_obj.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    print(f"Error parsing datetime: {e}")
                    publish_time = ''

                detail_url = url

                # 写入数据到CSV文件
                writer.writerow([title, text1, publish_time, source, image_urls_str, detail_url])

print("数据已成功保存到CSV文件。")
