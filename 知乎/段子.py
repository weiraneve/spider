# 获取某个知乎用户详细信息的API接口
user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
# 获取某个知乎用户关注了用户信息的API接口
followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
# 获取某个知乎用户关注者用户信息的API接口
followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'

import re
import os
import time
import random
import pickle
import requests


'''知乎段子'''
class zhihuJokesSpider():
    def __init__(self, question_id, **kwargs):
        self.question_id = question_id
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate'
            }
        self.api_url = 'https://www.zhihu.com/node/QuestionAnswerListV2'#api
        self.session = requests.Session()
        self.pointer = 0
        self.limits = 2000
    '''开始运行'''
    def start(self):
        offset = -1
        size = 1
        jokes = []
        while self.pointer <= self.limits:
            offset += size
            data = {
                    'method': 'next',
                    'params': '{"url_token":%s,"page_size":%s,"offset":%s}' % (self.question_id, size, offset)
                }
            response = self.session.post(self.api_url, headers=self.headers, data=data)
            joke = eval(response.text)['msg'][0].replace('\\', '')
            joke = re.findall(r'<p>(.*?)</p>', joke)
            joke_filtered = []
            for item in joke:
                if '<br>' in item: item = item.replace('<br>', '')
                if '<b>' in item: item = item.replace('<b>', '')
                if '</b>' in item: item = item.replace('</b>', '')
                if len(item) < 5: continue
                if 'www.zhihu.com' in item: continue
                joke_filtered.append(item)
            joke = '\n'.join(joke_filtered)
            with open("1.txt","a") as f:
                f.write(joke)
            #print(joke)
            time.sleep(random.randint(0, 1) + random.random())
            self.pointer += 1

if __name__ == '__main__':
    question_id = '341002197'#网页后缀id
    client = zhihuJokesSpider(question_id)
    client.start()
