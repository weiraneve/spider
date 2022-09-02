import csv,time,datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
options = webdriver.ChromeOptions() 
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chromedriver_path = "/usr/local/bin/chromedriver" #驱动路径
# driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
#先在终端打开： Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"

starttime = datetime.datetime.now()
print("启动时间：{0}".format(starttime))

def get_fans(name,url_name,path):
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options) 
    url = "https://twitter.com/{0}/followers".format(url_name)
    driver.get(url)
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    
    with open( path + '/{0}的粉丝.csv'.format(name),'a') as f: 
        zone = csv.writer(f)
        head = ['fans_name','fans_id']
        zone.writerows([head])
        
    old_scroll_height = -1
    js1 = 'return document.body.scrollHeight'  # 获取页面高度的javascript语句
    js2 = 'window.scrollTo(0, document.body.scrollHeight)' # 将页面下拉的Javascript语句
    all_limit = 100000 #总量要爬取多少粉丝数量 
    one_limit = 5000 #单次想要爬取多少数量
    frequecy = int(all_limit/one_limit) #循环次数
    num = 0
    data = set() #利用set不可重复性 
    flag = True
    
    while(flag):
        old_scroll_height = driver.execute_script(js1) #获得浏览器高度
        time.sleep(2)
        content = bs(driver.page_source, 'html.parser')  # 解析网页
        names = content.find_all(
            'div', 'css-901oao css-bfa6kz r-18jsvk2 r-1qd0xha r-a023e6 r-b88u0q r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0')  # 找到所有用户数据
        url_names = content.find_all(
            'div', 'css-901oao css-bfa6kz r-m0bqgq r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0')  # 找到所有用户数据
        followers_list = []
        url_list = []
        for followers_name in names[1:-3]:  #名字里带有表情的爬取的数据都是None
            followers_list.append(followers_name.string)  
        for url_name in url_names[1:-3]: #删去最开始的一个后最后三个名字
            url_list.append(url_name.string) #运用美味汤的API,一个网页大概31个
        for i in range(len(followers_list)):
            need_data = str(followers_list[i]) +'醠' + str(url_list[i]) #先用列表装，后利用set
            data.add(need_data)
        driver.execute_script(js2) # 模拟浏览器进行滚动下拉
        if (driver.execute_script(js1) > old_scroll_height): #检查是否到底,小用户
            pass
        else:
            time.sleep(2) #检查是否到底时常有bug，主要是网速波动影响
            driver.execute_script(js2) # 模拟浏览器进行滚动下拉
            time.sleep(2) 
            if (driver.execute_script(js1) == old_scroll_height):   #这个针对小用户比较适合。
                with open(path + '/{0}的粉丝.csv'.format(name),'a') as f: 
                    for write_data in data:
                        followers_name = write_data.split('醠')[0]
                        url_name = write_data.split('醠')[1]
                        zone = csv.writer(f)
                        zone.writerows([[followers_name,url_name]])
                print("{}名关注者爬取完毕".format(len(data))) 
                flag = False
#         --------大用户or小用户--------
        #鉴于效率和内存的综合考虑，现在将爬取大用户的程序分为多重循环，依次释放内存，进行爬取
        #鉴于特别容易出bug，暂且试试大用户不设定判断到底。
        #由于网络波动，发现接管的网页可能出错从而锁住进程，需要时常看看网页情况。
#         if len(data) >= one_limit:  # 判断是否达到指定的爬取数量，达到则跳出循环,大用户
#             num += 1
            with open(path + '/{0}的粉丝.csv'.format(name),'a') as f: 
                for write_data in data:
                    followers_name = write_data.split('醠')[0]
                    url_name = write_data.split('醠')[1]
                    zone = csv.writer(f)
                    zone.writerows([[followers_name,url_name]])
                print("{}名关注者爬取完毕".format(len(data))) 
#             endtime = datetime.datetime.now()
#             print("第{0}部分已经爬取完成--{1}".format(num,endtime))
#             followers_name_data.clear()
#             url_name_data.clear() #清空元素,释放内存
#         if (num >= frequecy):
#             flag = False
            
get_fans(name = 'e',url_name='nana_blacq',path='')

# 正常速度7分钟5k，网络波动后15分钟+爬5K。但set没有排序。
