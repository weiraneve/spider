import requests,re

def split_cookies(raw_cookie):# 拆分cookies
    raw_cookies = '{raw_cookie}'.format(raw_cookie=raw_cookie)# Chrome上直接复制下的cookie值
    keys = []    # 申明键和值的列表
    values = []
    cookie_list = raw_cookies.split(";")    # 先根据;拆分各个cookie，得到cookie_list列表
    for item in cookie_list:    # 再根据 = 拆分键和值
        keys.append(item.split('=', 1)[0])
        values.append(item.split('=', 1)[1])
    cookies = dict(zip(keys, values))
    return cookies

def get_data_usecookies(url):#需要使用cookies的模块
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    raw_cookies =""#网页里寻找
    cookies = split_cookies(raw_cookies)
    r = requests.get(url, headers=headers, cookies = cookies)
    r.raise_for_status()
    return r.text

def get_data(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.text

def parse_data_usecookies(url):#需要使用cookies的模块
    html = get_data_usecookies(url)
    pattern = '<span>他<!-- -->赞同我'  
    flag = re.search(pattern,str(html))
    if flag:
        return True
    else:
        return False   

def parse_data(url):
    html = get_data(url)
    pattern = '<span>他<!-- -->赞同我'  
    flag = re.search(pattern,str(html))
    if flag:
        return True
    else:
        return False   

def main():
    count = 0
    all_count = 0
    for i in range(1,194):
        url = "https://www.zhihu.com/people/feng-ye-xiao-wo/followers?page={0}".format(i)
        html = get_data(url)
        pattern = '"urlToken":"(.[^"]+)'  
        names = re.findall(pattern,str(html))
        names.pop(0)
        names.pop()
        for name in names:
            all_count += 1
            url = "https://www.zhihu.com/people/{0}".format(name)
            if parse_data_usecookies(url) :
                count += 1
    print("总共有{0}".format(all_count))
    print("有高质量关注者{0}".format(count))
        
if __name__ == "__main__":
    main()
    print("完成！！！")
    
