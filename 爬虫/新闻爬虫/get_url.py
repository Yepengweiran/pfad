from lxml import html
import requests
import os

url_dict = {
    '国内': 'https://www.chinanews.com.cn/china.shtml',
    '国际': 'https://www.chinanews.com.cn/world.shtml',
    '社会': 'https://www.chinanews.com.cn/society.shtml',
    '财经': 'https://www.chinanews.com.cn/cj/gd.shtml',
    '体育': 'https://www.chinanews.com.cn/sports.shtml',
    '文娱': 'https://www.chinanews.com.cn/wenhua.shtml'
}

xpath = '/html/body/div[4]/div[1]/div[2]/ul/li/div[2]/a/@href'

script_dir = os.path.dirname(os.path.abspath(__file__))
news_dir = os.path.join(script_dir, 'news_url')

if not os.path.exists(news_dir):
    os.makedirs(news_dir)

for category, url in url_dict.items():
    response = requests.get(url)
    
    tree = html.fromstring(response.content)
    
    hrefs = tree.xpath(xpath)
    
    total_links = len(hrefs)
    
    filename = f"{category}{total_links}.txt"
    
    full_path = os.path.join(news_dir, filename)
    
    with open(full_path, 'w', encoding='utf-8') as file:
        for href in hrefs:
            news_link = 'https://www.chinanews.com' + href
            file.write(f"{news_link}\n")
    
    print(f"Category '{category}' has {total_links} links saved to {filename}")