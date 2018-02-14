# 3:55 PM, Feb 14th, 2018 @ home, Shangyu
# 技术关键词：Requests, re, 正则式
# 爬取糗事百科的段子信息
# 爬取的内容：用户ID、用户等级、用户性别、发表段子、好笑指数、评论数量
# 先爬取用户ID、发表段子、好笑指数试试看看

# urls:
# https://www.qiushibaike.com/text/page/1/
# https://www.qiushibaike.com/text/page/2/
# https://www.qiushibaike.com/text/page/3/
# ...
# https://www.qiushibaike.com/text/page/13/

import requests
import time
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
info_list = []

def manOrwoman(classname):
    if classname == 'manIcon':
        return 'man'
    if classname == 'womenIcon':
        return 'woman'
    else:
        return 'neuter'

def getInfo(url):
    res = requests.get(url, headers=headers)
    IDs = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    genders = re.findall('<div class="articleGender (.*?)">.*?</div>', res.text)
    ranks = re.findall('<div class="articleGender.*?">(.*?)</div>', res.text)
    contents = re.findall('<div class="content">[\n]<span>(.*?)</span>.*?</div>', res.text, re.S)
    laughs = re.findall('<span class="stats-vote"><i class="number">(.*?)</i>.*?</span>', res.text)
    comments = re.findall('<span class="stats-comments">[\n].*?[\n].*?[\n]<i class="number">(.*?)</i>', res.text)
    for ID, gender, rank, content, laugh, comment in zip(IDs, genders, ranks, contents, laughs, comments):
        info = {
            'ID': ID.strip(),
            'gender': manOrwoman(gender),
            'rank': rank.strip(),
            'content': content.strip(),
            'laugh': laugh,
            'comment': comment
        }
        info_list.append(info)

def main():
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(page) for page in range(1, 14)]
    for url in urls:
        getInfo(url)
        time.sleep(1)
    file = open('E:\AllPrj\PyCharmPrj\py-crawler\爬取糗事百科的段子\糗事百科段子.txt', 'w+', encoding='utf-8')
    for info in info_list:
        print(info)
        file.write('ID:' + info['ID'] + '\n')
        file.write('gender:' + info['gender'] + '\n')
        file.write('等级：' + info['rank'] + '\n')
        file.write('爆料:' + info['content'] + '\n')
        file.write('爆笑指数：' + info['laugh'] + '\n')
        file.write('评论数量：' + info['comment'] + '\n')
        file.write('\n')
    file.close()
if __name__ == '__main__':
    main()


