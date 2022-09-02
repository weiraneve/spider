from selenium import webdriver
options = webdriver.ChromeOptions() 
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chromedriver_path = "/usr/local/bin/chromedriver" #驱动路径
browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
#直接selenium接管浏览器Chrome，并且可以在Chrome上关闭图片加载以加快爬虫速度
#先在终端打开： Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"

url=''
browser.get(url)
#写入cookies
cookies = {}
cks = browser.get_cookies()
for ck in cks:
    cookies[ck['name']] = ck['value']
ck1 = json.dumps(cookies)
with open('ck.txt','w') as f :
    f.write(ck1)

print(browser.page_source) #源代码
