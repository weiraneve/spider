import requests,json,re,os
from bs4 import BeautifulSoup
from selenium import webdriver

def get_source(url):
    page = url.split("?")[-1]#取出page
    page = page + '.txt'
    if not os.path.exists(page): 
        browser = webdriver.Chrome()
        browser.get(url)
        html = browser.page_source
        with open(page ,'a') as f:
            f.write(html)#文件不存在，则开启webdriver写
        browser.close()
    else:
        with open(page ,'r+') as f:
            html = f.read()
    return html

def parse(html):   
    soup = BeautifulSoup(html, 'lxml')
    namelist = soup.findAll("a",{'target' :'_blank'})
    pattern = 'question(.[^<]+)'#href= 到 <为止的数据    
    contents = re.findall(pattern,str(namelist))
    for content in contents:
        with open("所需网址.txt","a") as f:
            content = content.replace("\" target=\"_blank\">","   ")
            f.write("www.zhihu.com/question"+str(content) + "\n\n")
for i in range(1,3):
    url = "https://www.zhihu.com/people/liaoxuefeng/answers"#所填
    url = url + "?page={0}".format(i)
    source = get_source(url)
    parse(source)
