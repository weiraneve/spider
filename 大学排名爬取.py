import requests
from bs4 import BeautifulSoup
import bs4
import csv


def get_content(url,):
    try:
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"
        response = requests.get(url,  headers={'User-Agent': user_agent})
        response.raise_for_status()   # 如果返回的状态码不是200， 则抛出异常;
        response.encoding = response.apparent_encoding  # 判断网页的编码格式， 便于respons.text知道如何解码;
    except Exception as e:
        print("爬取错误")
    else:

        print(response.url)
        print("爬取成功!")
        return  response.content



def getUnivList(html):
    """解析页面内容， 需要获取: 学校排名， 学校名称， 省份， 总分"""
    soup = BeautifulSoup(html, 'lxml')
    # 该页面只有一个表格， 也只有一个tbody标签;
    # 获取tbosy里面的所有子标签, 返回的是生成器： soup.find('tbody').children
    # 获取tbosy里面的所有子标签, 返回的是列表：   soup.find('tbody').contents
    uList = []
    for tr in soup.find('tbody').children:
        # 有可能没有内容， 获取的tr标签不存在, 判断是否为标签对象?
        if isinstance(tr, bs4.element.Tag):
            # print(tr.td)
            # 返回tr里面的所有td标签;
            tds = tr('td')
            # print(tds)
            # 将每个学校信息以元组的方式存储到列表变量uList中;
            uList.append((tds[0].string, tds[1].string, tds[2].string, tds[3].string))
    return  uList


def printUnivList(uList):
    """
    打印学校信息
    :param uList:
    :return:
    """
    # format的使用: {0} 变量的位置, 冒号后面执行属性信息: ^10占10个字节位置， 并且居中
    print("{0:^10} {1:^10} {2:^10} {3:^10}".format("排名", '学校名称', "省份/城市", "总分"))
    for item in uList:
        # print(item)
        print("{0:^10} {1:^10} {2:^10} {3:^10}".format(item[0], item[1], item[2], item[3]))



def saveUnivData(uList, year):

    with open('{0}学校排名.csv'.format(year) , 'a') as f:
        writer = csv.writer(f)
        # 将列表的每条数据依次写入csv文件， 并以逗号分隔
        writer.writerows(uList)
        print("写入完成....")


if __name__ == '__main__':
    start_year = int(input("开始爬取的年份:"))
    end_year =  int(input("结束爬取的年份:"))
    for year in range(start_year, end_year+1):
    # year = 2017
        url = "http://www.zuihaodaxue.com/zuihaodaxuepaiming%s.html" %(year)
        content = get_content(url)
        uList = getUnivList(content)
        # printUnivList(uList)
        saveUnivData(uList, year)
        print("%s年信息爬取成功......" %(year))


