from selenium import webdriver
import json

#写入cookies
cookies = {}
browser.get(url)
cks = browser.get_cookies()
for ck in cks:
    cookies[ck['name']] = ck['value']
ck1 = json.dumps(cookies)
with open('ck.txt','w') as f :
    f.write(ck1)
#读取cookies    
with open('ck.txt','r') as f :
    cookies = f.read()
    cookies = json.loads(cookies)
