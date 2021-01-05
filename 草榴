import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
chrome_opt = Options()
chrome_opt.add_argument("--headless")  # => 为Chrome配置无头模式
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
ID = 0

def put_db(title,url):
    db = pymysql.connect(host='localhost', port=3306,
    user='root', passwd='sun8100512', db='caoliu', charset='utf8')
    cursor = db.cursor()    # 使用cursor()方法获取操作游标
    sql = "INSERT INTO rawdata(ID,url,url_md5,cat,cat_name,title) VALUES (%s,%s,%s,%s,%s,%s)"
    #cat_name为分类，title为帖子名字
    global ID
    ID += 1
    insert = [(ID,url,ID,'1','技术讨论区',title)]   # 一个tuple或者list
    try:
        cursor.executemany(sql, insert)      # 执行sql语句
        db.commit()       # 提交到数据库执行
    except Exception as e: 
        db.rollback()      # 如果发生错误则回滚
        print('发生错误')
        print(e)
    cursor.close()      #关闭游标
    db.close()    # 关闭数据库连接
    
def get_webdriver(pages):
#     browser = webdriver.Chrome(options=chrome_opt)  # 在启动浏览器时加入配置，无头浏览器配置
    browser = webdriver.Chrome()
#     url = 'http://www.t66y.com/thread0806.php?fid=7' #技术讨论区
    url = "http://www.t66y.com/thread0806.php?fid=7&search=&page={0}".format(pages)
    browser.get(url)
    for count in range(12,100): #第一页是从12到105，之后一直到100页都是3到102
        title = browser.find_element_by_xpath('//*[@id="ajaxtable"]/tbody[2]/tr[{0}]/td[2]/h3/a'.format(count)).text
        url = browser.find_element_by_xpath('//*[@id="ajaxtable"]/tbody[2]/tr[{0}]/td[2]/h3/a'.format(count)).get_attribute("href")
        put_db(title,url) 
    browser.quit()

# get_webdriver(0)
for i in range(0,100):
    get_webdriver(i)
