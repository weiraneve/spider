import re
import requests
from selenium import webdriver
import time
from urllib import parse

class get_list():
    def __init__(self):
        self.qq_list = []

    def Login_QQ(self):
        '''gtk解密'''

        def getGTK(cookie):
            """ 根据cookie得到GTK """
            hashes = 5381
            for letter in cookie['p_skey']:
                hashes += (hashes << 5) + ord(letter)
            gtk = hashes & 0x7fffffff
            return gtk

        browser = webdriver.Chrome()
        url = "https://qzone.qq.com/"  
        browser.get(url)
        print("正在执行登录操作")
        time.sleep(10)
        print("睡眠时间结束, 登录")
        print(browser.title)  # 打印网页标题
        cookie = {}
        for element in browser.get_cookies():
            cookie[element['name']] = element['value']
        html = browser.page_source  
        pattern = re.compile(r'window\.g_qzonetoken = \(function\(\)\{ try\{return "(.*?)";\}')
        g_qzonetoken = re.search(pattern, html)
        g_qzonetoken = g_qzonetoken.group(1)
        gtk = getGTK(cookie) 
        browser.close()
        qq = '907221539'#账号
        self.get_friends_url (qq,cookie,gtk,g_qzonetoken)
        return self.qq_list

    def get_friends_url(self,qq,cookie,gtk,qzonetoken):
        url='https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?'
        params = {"uin": qq,
              "fupdate": 1,
              "action": 1,
             'qzonetoken': qzonetoken,
              "g_tk": gtk}
        url = url + parse.urlencode(params)
        cookie = cookie
        headers = {
        'Host': 'user.qzone.qq.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
        self.get_friends_num(url,headers,cookie)

    def get_friends_num(self,url,headers,cookie):
        offset= 300 #有多少好友,设为50倍数
        qq_list = []
        for i in range(0,offset,50):
            qq_url = url+'&offset='+str(i)
            page = requests.get(url= qq_url, headers= headers,cookies = cookie).text
            qq_url = url
            qq_num = re.findall('"data":"(\w+)',page)
            qq_list = qq_list + qq_num
        self.qq_list = qq_list


