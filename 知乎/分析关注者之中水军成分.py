import requests,re

def get_data(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")
        
def parse_water(url):
    html = get_data(url)
    pattern = 'class="NumberBoard-itemValue" title=(.[^"]+)'  
    num = re.findall(pattern,str(html))#num[0]为关注了，num[1]为关注者。
    try:
        num[0] = num[0].replace('\"',"")#出去里面的引号
        num[1] = num[1].replace("\"","")
        if (num[0] == '53') & (num[1] == '0'):#关注了53，关注者为0的人很可能是水军。
            return True
        else:
            return False
    except IndexError :
        pass

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
            if parse_water(url) :
                count += 1
    print("总共有{0}".format(all_count))
    print("有水军{0}".format(count))
        
if __name__ == "__main__":
    main()
    print("完成！！！")
    
