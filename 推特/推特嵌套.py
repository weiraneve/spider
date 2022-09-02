import os,csv,time,datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
options = webdriver.ChromeOptions() 
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chromedriver_path = "/usr/local/bin/chromedriver" #驱动路径
# driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
#先在终端打开： Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"

all_count = 0

def get_fans(file_url_name,path):
    starttime = datetime.datetime.now()
    print("启动时间：{0}".format(starttime))
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options) 
    url = "https://twitter.com/{0}/followers".format(file_url_name)
    driver.get(url)
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    
    with open( path + '/{0}的粉丝.csv'.format(file_url_name),'a') as f: 
        zone = csv.writer(f)
        head = ['fans_id']
        zone.writerows([head])
        
    old_scroll_height = -1
    js1 = 'return document.body.scrollHeight'  # 获取页面高度的javascript语句
    js2 = 'window.scrollTo(0, document.body.scrollHeight)' # 将页面下拉的Javascript语句
    all_limit = 50000 #总量要爬取多少粉丝数量 
    one_limit = 1000 #单次想要爬取多少数量
    frequecy = int(all_limit/one_limit) #循环次数
    num = 0
    url_data = set() #利用set不可重复性 
    flag = True
    
    while(flag):
        old_scroll_height = driver.execute_script(js1) #获得浏览器高度
        time.sleep(2)
        content = bs(driver.page_source, 'html.parser')  # 解析网页
        #name需要'div', 'css-901oao css-bfa6kz r-18jsvk2 r-1qd0xha r-a023e6 r-b88u0q r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0'
        #名字里带有表情的爬取的数据都是None，此处只爬取url_name，放弃name
        url_names = content.find_all(
            'div', 'css-901oao css-bfa6kz r-m0bqgq r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0')  # 找到所有用户数据
        for url_name in url_names[1:-3]: #删去最开始的一个后最后三个名字
            url_data.add(url_name.string) #运用美味汤的API,一个网页大概31个
        driver.execute_script(js2) # 模拟浏览器进行滚动下拉
        
#         if len(url_data) >= all_limit: #爬取达到设定数量，写入
#             with open(path + '/{0}的粉丝.csv'.format(file_url_name),'a') as f: 
#                 for url_name in url_data:
#                     zone = csv.writer(f)
#                     zone.writerows([[url_name]])
#             print("{}名关注者爬取完毕".format(len(url_data))) 
#             global all_count
#             all_count += len(url_data)
#             print("已经有{}名关注者爬取完毕".format(all_count))
#             flag = False
                
#         if (driver.execute_script(js1) > old_scroll_height): #检查是否到底,针对小用户---
#             pass #小用户爬取受网络波动影响很大，很容易只爬取几个粉丝就开始下一个网页的跳转
#         else:
#             time.sleep(2) #检查是否到底时常有bug，主要是网速波动影响
#             driver.execute_script(js2) # 模拟浏览器进行滚动下拉
#             time.sleep(2) 
#             if (driver.execute_script(js1) == old_scroll_height):   #这个针对小用户比较适合。
#                 with open(path + '/{0}的粉丝.csv'.format(file_url_name),'a') as f: 
#                     for url_name in url_data:
#                         zone = csv.writer(f)
#                         zone.writerows([[url_name]])
#                 print("{}名关注者爬取完毕".format(len(url_data))) 
# #                 global all_count
#                 all_count += len(url_data)
#                 print("已经有{}名关注者爬取完毕".format(all_count))
#                 flag = False
#         --------大用户or小用户--------
#         鉴于效率和内存的综合考虑，现在将爬取大用户的程序分为多重循环，依次释放内存，进行爬取
#         鉴于特别容易出bug，暂且试试大用户不设定判断到底。
#         由于网络波动，发现接管的网页可能出错从而锁住进程，需要时常看看网页情况。
        if len(url_data) >= one_limit:  # 判断是否达到指定的爬取数量，达到则跳出循环,大用户
            num += 1
            with open(path + '/{0}的粉丝.csv'.format(file_url_name),'a') as f: 
                for url_name in url_data:
                    zone = csv.writer(f)
                    zone.writerows([[url_name]])
                print("{}名关注者爬取完毕".format(len(url_data))) 
            endtime = datetime.datetime.now()
            print("第{0}部分已经爬取完成--{1}".format(num,endtime))
            url_data.clear() #清空元素,释放内存
        if (num >= frequecy):
            flag = False
            
get_fans(file_url_name='KDTrey5',path='/Users/shanshan/Desktop/python')

# 正常速度7分钟5k，网络波动后15分钟+爬5K。但set没有排序。

#---------


def fans_to_fans(origin_path):  
    #将这个文件夹里的csv文件遍历，然后在此路径下创建子文件夹以及子文件夹中的粉丝数据csv文件
    name = str(origin_path)
    name = name.split('/')[-1]
    with open('{0}/{1}的粉丝.csv'.format(origin_path,name), 'r') as f: #读取csv
        reader = csv.reader(f)
        count = 0 
        max_limit = 100
        for row in reader:
            count += 1
            if (count != 1): # #不取1
                url_name = row[0]
                url_name = url_name.split("@")[1]
                path = "{0}/{1}".format(origin_path,url_name) #路径文件夹是否存在
                isExists = os.path.exists(path) 
                if not isExists: #不存在则创建文件夹
                    os.mkdir(path) 
                get_fans(url_name,path)
            elif count > max_limit:
                return #大于限制后提前结束  

def fans_three(origin_path): #遍历这个根目录文件名路径下的所有子文件夹名字
    result = os.listdir(origin_path) #最初的根文件夹名
    for file_name in result:
        if (file_name[0] == '.') | (file_name[-4:] == '.csv'):
            pass
        else :
            file_name = origin_path + '/' + file_name
            fans_to_fans(file_name)  #调用函数


# origin_path = "/Users/shanshan/Desktop/python/KingJames" #根目录文件名
# fans_to_fans(origin_path) #先执行这一行语句，遍历根目录
# fans_three(origin_path)
----------------------------
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options) 

for i in range(20,25):  # 点击刷新
    for j in range(2,4):
        try :
            driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div[{0}]/div/div/div[{1}]/div/span/span'.format(i,j)
                                    ).click()
        except:
            pass
# 我们需要的方案是去检测，出现加载的符号出现时，程序等待，没有出现且浏览器滑到底时，跳转。

----------------------------

def fans_to_fans(origin_path):  
    #将这个文件夹里的csv文件遍历，然后在此路径下创建子文件夹以及子文件夹中的粉丝数据csv文件
    name = str(origin_path)
    name = name.split('/')[-1]
    with open('{0}/{1}的粉丝.csv'.format(origin_path,name), 'r') as f: #读取csv
        reader = csv.reader(f)
        count = 0 
        max_limit = 100
        for row in reader:
            count += 1
            if (count != 1): # #不取1
                url_name = row[0]
                url_name = url_name.split("@")[1]
                path = "{0}/{1}".format(origin_path,url_name) #路径文件夹是否存在
                isExists = os.path.exists(path) 
                if not isExists: #不存在则创建文件夹
                    os.mkdir(path) 
#                 get_fans(url_name,path)
            elif count > max_limit:
                return #大于限制后提前结束  
fans_to_fans("/Users/shanshan/Desktop/python/doublelift1")

def fans_three(origin_path): #遍历这个根目录文件名路径下的所有子文件夹名字
    result = os.listdir(origin_path) #最初的根文件夹名
    for file_name in result:
        if (file_name[0] == '.') | (file_name[-4:] == '.csv'):
            pass
        else :
            file_name = origin_path + '/' + file_name
            fans_to_fans(file_name)  #调用函数
        
origin_path = "/Users/shanshan/Desktop/python/doublelift1" #根目录文件名
fans_three(origin_path)


----------------------------
import os 
print(os.path.abspath('.'))

def fans_three(origin_path):
    result = os.listdir(origin_path) #最初的根文件夹名
    for file_name in result:
        if (file_name[0] == '.') | (file_name[-4:] == '.csv'):
            pass
        else :
            file_name = origin_path + '/' + file_name
            print(file_name)
origin_path = origin_path = "/Users/shanshan/Desktop/python/doublelift1"
fans_three(origin_path)
----------------------------
import csv

names = ["KingJames的粉丝","AntDavis23的粉丝","JHarden13的粉丝","KDTrey5的粉丝","russwest44的粉丝","StephenCurry30的粉丝"]
for name in names:    
    data = pd.read_csv("/Users/shanshan/Desktop/python/KingJames的粉丝/{0}/{0}.csv".format(name),encoding="gbk")#一开始可能要用 gbk 后面重新保存为csv，可以用utf-8了
    data = data.drop_duplicates(subset=None, keep='first', inplace=False) #过滤
#     print(len(data))
    data.to_csv("/Users/shanshan/Desktop/python/KingJames的粉丝/{0}/{0}.csv".format(name),
                index = False) #index 控制不写行名字
    with open('/Users/shanshan/Desktop/python/KingJames的粉丝/{0}/{0}.csv'.format(name), 'r') as f: #读取csv
        reader = csv.reader(f)
        with open('all.csv','a') as f1: 
            zone = csv.writer(f1)
            zone.writerows(reader)

all_csv = pd.read_csv("all.csv",encoding="utf-8")#一开始可能要用 gbk 后面重新保存为csv，可以用utf-8了
filter_all = all_csv.drop_duplicates(subset=None, keep='first', inplace=False) #过滤
print(len(all_csv))
print(len(filter_all))
filter_all.to_csv("filter_all.csv",
            index = False) #index 控制不写行名字

