import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import snownlp

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
file_path = './新闻爬虫/news_data.csv'
news_data = pd.read_csv(file_path)

# 数据预处理
news_data_cleaned = news_data.dropna().drop_duplicates()
news_data_cleaned['publish_time'] = pd.to_datetime(news_data_cleaned['publish_time'])
news_data_cleaned = news_data_cleaned[['title', 'content', 'publish_time', 'source']]

# 读取停用词表并清理特殊字符
with open('./情感分析/stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = f.read().splitlines()
    stopwords = [word for word in stopwords if word.strip() and not any(char.isdigit() for char in word)]

# 趋势分析

# 按周统计新闻数量
news_data_cleaned['week'] = news_data_cleaned['publish_time'].dt.to_period('W')
weekly_trend = news_data_cleaned.groupby('week').size()

plt.figure(figsize=(10, 6))
weekly_trend.plot(kind='line')
plt.title('Weekly News Count')
plt.xlabel('Week')
plt.ylabel('Number of News')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()