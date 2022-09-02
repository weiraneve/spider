#简单知乎文字爬取
import requests
from pyquery import PyQuery as pq#pyquery解析库
def get_words(url):
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    html = requests.get(url,headers = headers).content
    doc = pq(html)
    lis=(doc.find('p'))
    item = lis.items()
    for item1 in item:
        print(item1.text())
#分隔线---------------------------------------------------------------------------------------------------------------------

#爬知乎的照片
from bs4 import BeautifulSoup   
import requests                 
import os 
import random

root = ''#设定文件名字—————————————————————————————————————————————————————————————————————
url = '' #设定网址—————————————————————————————————————————————————————————————————————
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
r = requests.get(url,headers = headers)                      
r.encoding='utf-8'                         
num = 0
if r.status_code!=404:                      
    demo = r.text                           
    soup = BeautifulSoup(demo, "lxml")
    text = soup.findAll('img')
    for img in text:
        imagr_url = img.get('src')  
        num = num +1
        if num > 100: #数量设定处——————————————————————————————————————————————————————————————————————
            break
        else :    
            file_name = root + str(num)+'.jpg' 
        try:
            if not os.path.exists(root):            
                os.mkdir(root)
            if not os.path.exists(file_name):       
                s = requests.get(imagr_url)         
                path = '/Users/guohezu/Desktop/python/'+ str(root)
                a_path = os.path.join(path, file_name)
                with open(a_path, "wb") as f:  
                    f.write(s.content)
                print("爬取完成")
            else:
                print("文件已存在")
        except Exception as error:
            print("爬取失败:" + str(error))#让爬取失败不影响整体爬取
