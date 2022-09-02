import time , json ,random
import csv , requests,re
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import html
import os , pdfkit

# 获取cookies和token
class C_ookie(object):
    # 初始化
    def __init__(self):
        self.html = ''
    # 获取cookie
    def get_cookie(self):
        cooki = {}
        url = 'https://mp.weixin.qq.com'
        Browner = webdriver.Chrome()#不输入账号密码，直接扫码
        Browner.get(url)
        # 等待扫二维码
        time.sleep(12)
        cks = Browner.get_cookies()
        for ck in cks:
            cooki[ck['name']] = ck['value']
        ck1 = json.dumps(cooki)
        with open('ck.txt','w') as f :
            f.write(ck1)
            f.close()
        self.html = Browner.page_source
        
# 获取文章
class getEssay:

    def __init__(self):
        # 获取cookies
        with open('ck.txt','r') as f :
            cookie = f.read()
            f.close()
        self.cookie = json.loads(cookie)

        # 获取token
        self.header = {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": 'Mozilla / 5.0(WindowsNT6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 74.0.3729.131Safari / 537.36'
        }
        m_url = 'https://mp.weixin.qq.com'
        response = requests.get(url=m_url, cookies=self.cookie)
        self.token = re.findall(r'token=(\d+)', str(response.url))[0]
        # fakeid与name
        self.fakeid = []


    # 获取公众号信息
    def getGname(self):
        # 请求头
        headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'mp.weixin.qq.com',
        'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=%d&lang=zh_CN'%int(self.token),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
         }
        # 地址
        url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        # query = input('请输入要搜索的公众号关键字:，也可以输入公众号编号，准确寻找')------------------------------------------------------------------------------------------------------------
        query = ''
        # 请求参数
        data = {
            'action': 'search_biz',
            'token': self.token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax':' 1',
            'random': random.random(),
            'query': query,
            'begin': 0 ,
            'count': '5'
        }
        # 请求页面，获取数据
        res = requests.get(url=url, cookies=self.cookie, headers=headers, params=data)
        name_js = res.text
        name_js = json.loads(name_js)
        list = name_js['list']
        for i in list:
            time.sleep(1)
            fakeid = i['fakeid']
            nickname =i['nickname']
            print(nickname)
            self.fakeid.append((nickname,fakeid))

    # 获取文章url
    def getEurl(self):

        url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'mp.weixin.qq.com',
        'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=%d&lang=zh_CN'%int(self.token),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
         }
        for begin in range(20,181,5): 
        #begin,为爬取多少页------------------------------------------------------------------------------------------------------------------------------------------------------
        # 遍历fakeid，访问获取文章链接
            for i in self.fakeid:
                time.sleep(1)
                fake = i[1]
                data = {
                    'token': self.token,
                    'lang': 'zh_CN',
                    'f': 'json',
                    'ajax': '1',
                    'random': random.random(),
                    'action': 'list_ex',
                    'begin': begin, #关键
                    'count': 5,
                    'fakeid': fake,
                    'type': 9
                    }
                res = requests.get(url, cookies=self.cookie, headers=headers, params=data)
                js = res.text
                link_l = json.loads(js)
                self.parJson(link_l)

    # 解析提取url
    def parJson(self,link_l):
        l = link_l['app_msg_list']
        for i in l:
            link = i['link']
            name = i['title']
            self.saveData(name,link)

    # 保存数据
    def saveData(self,name,link):
        with open('link.csv' ,'a',encoding='utf8') as f:
            w = csv.writer(f)#保存为csv
            w.writerow((name,link))
            #pdfkit.from_url(link,'{0}.pdf'.format(name)) #内容保存为pdf
        url = link
        response = requests.get(url).text
        soup = BeautifulSoup(response,'lxml')
        words = soup.findAll('span')
        path = ''#存储地址
        file_name = str(name.replace('/',''))+'.txt'#文件格式里不能有‘/’，对应mac
        a_path = os.path.join(path,file_name)
        for word in words:
            with open(a_path,'a') as f:#追加a
                word = word.get_text()
                f.write(word)#保存正文
        print('爬取完毕')
        

C = C_ookie()
C.get_cookie()
G = getEssay()
G.getGname()
G.getEurl()
