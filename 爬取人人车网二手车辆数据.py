from bs4 import BeautifulSoup as bs
import requests 
import random,csv

def get_cars_in_Page(url):
    host = 'https://www.renrenche.com'
    proxies = { 
        'http' : 'http://201.69.7.108:9000',
    }  #更换IP池
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36','Accept-Language':'zh-CN','Cache-Control':'no-cache'}
    r = requests.get(url, headers = headers,timeout = 1,proxies = proxies)#老实讲好像这里很容易被封IP，爬了一会被封了
    soup = bs(r.text,'lxml')
    cars = soup.select('div.container.search-list-wrapper a')
    for car in cars:
        car_url = host + car.get('href')
        get_info_from(car_url) #将每一页获得的具体车俩的网址带入get_info_from方法中

def get_info_from(url):
    ua = 'Mozilla/5.0 (Windows NT 6.1;) AppleWebKit/532.5 (KHTML, like Gecko) Safari/532.5'
    headers = {'User-Agent': ua}
    r = requests.get(url,headers = headers, timeout = 2)
    soup = bs(r.text, 'lxml')   
    try:
        title = soup.find('h1',class_ ='title-name').text
    except AttributeError:
        return; #数据为空则跳出函数
    new_price = soup.find('div',class_='list').find_all('p')[0].text
    old_price =  soup.find('div',class_='list').find_all('span')[1].text
    inf = soup.select('div.row-fluid-wrapper  strong')
    other_info = soup.find('div',class_='info-about-car').text.replace('\xa0','')
    dic = {
        '名称':title,
        '现价' :new_price,
        '全新价':old_price,
        '上牌年月':inf[0].text,
        '已开里程':inf[1].text,
        '排放等级':inf[2].text,
        '排量'    :inf[3].text,
        '其他信息': other_info
    }
    with open('二手车数据.csv','a') as f: #csv文件
        global count
        count += 1 #计数爬取了多少条车辆的数据
        data = csv.writer(f)
        data.writerows([[dic['名称'],dic['现价'],dic['全新价'],dic['上牌年月'],
                         dic['已开里程'],dic['排放等级'],dic['排量'],dic['其他信息']]])
    
def csv_write_head():
    dic = {
    '名称':'名称',
    '现价' :'现价',
    '全新价':'全新价',
    '上牌年月':'上牌年月',
    '已开里程':'已开里程',
    '排放等级':'排放等级',
    '排量'    :'排量'   ,
    '其他信息': '其他信息'
}
    with open('二手车数据.csv','a') as f: #csv文件
        data = csv.writer(f)
        data.writerows([[dic['名称'],dic['现价'],dic['全新价'],dic['上牌年月'],
                         dic['已开里程'],dic['排放等级'],dic['排量'],dic['其他信息']]])
count = 0 #全局变量
def main():
    csv_write_head()#给csv写上首行
#     url = 'https://www.renrenche.com/suz/car/5e3d2f58b560eef7'
#     get_info_from(url) #测试
    for i in range(1, 5): 
        url = 'https://www.renrenche.com/suz/ershouche/p{}/'.format(i) 
        get_cars_in_Page(url)
    print("总共爬取了{0}条数据".format(count))

main()


