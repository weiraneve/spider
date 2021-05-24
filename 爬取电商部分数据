import requests,re,time,csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none" #懒加载模式，不等待页面加载完毕
options = webdriver.ChromeOptions() 
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chromedriver_path = "/usr/local/bin/chromedriver" #驱动路径
browser = webdriver.Chrome(executable_path=chromedriver_path, 
                           options=options,desired_capabilities=capa)

#直接selenium接管浏览器Chrome，并且可以在Chrome上关闭图片加载以加快爬虫速度
#先在终端打开： Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"

def get_content(url):
    try:
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.110 Safari/537.36"
        response = requests.get(url,  headers={'User-Agent': user_agent})
        response.raise_for_status()   # 如果返回的状态码不是200， 则抛出异常;
        response.encoding = response.apparent_encoding  # 判断网页的编码格式， 便于respons.text知道如何解码;
    except Exception as e:
        print("爬取错误")
    else:
        return  response.text

def get_url(base_url):
    base = get_content(base_url)
    # print(base)
    base_url = re.findall("([a-zA-z]+://[^\s]*)(\" target=\"_blank\" class=\"f14sc\">)",base)
    url_name = re.findall("(class=\"f14sc\">)([^\x00-\xff]+)",base)
    url_list = []
    url_name_list = []
    for one_url in base_url:
        one_url = str(one_url).split("com%2f") 
        one_url = str(one_url[1]).split(".html")
        one_url = one_url[0]                        
        url_list.append(int(one_url))
    for one_name in url_name:
        url_name_list.append(one_name[1])
    return url_list,url_name_list

url = "http://www.b1bj.com/s.aspx?PageID=1&smallclass=&ppid=&siteid=1&price1=0&price2=0&orderby=&iszy=0&key=足疗器&iswap=0&NotContains=&proid=0"
url_list = []
url_name_list = []
all_list = get_url(url)
url_list = all_list[0] 
url_name_list = all_list[0]

def analyse():
    for page in range(1,2):
#         base_url = "http://www.b1bj.com/s.aspx?PageID={0}&smallclass=&ppid=&siteid=1&price1=0&price2=0&orderby=&iszy=0&key=足疗器&iswap=0&NotContains=&proid=0".format(page)        
#         url_list = get_url(base_url)
        print(url_list)
        for url_num in url_list:
            url = "https://item.jd.com/{0}.html?cu=true&utm_source=c.duomai.com&utm_medium=tuiguang&utm_campaign=t_16282_138786076&utm_term=79df51410d3c45e8a306aa2dd8a6deba#comment".format(url_num)  
            browser.get(url)
            time.sleep(3)
            source = browser.page_source
            bad = re.search("差评<em>\(\d+",source)
            mid = re.search("中评<em>\(\d+",source)
            good = re.search("好评<em>\(\d+",source)
            bad_num = re.search("\d+",str(bad)).group()
            mid_num = re.search("\d+",str(mid)).group()
            good_num = re.search("\d+",str(good)).group()
            print("差评: " + str(bad_num))
            print("中评: " + str(mid_num))
            print("好评: " + str(good_num))
analyse()

with open('统计.csv','a') as f:
    zone = csv.writer(f)
    zone.writerows()
