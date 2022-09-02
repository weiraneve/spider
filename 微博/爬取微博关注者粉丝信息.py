from urllib.parse import urlencode  
import requests, csv
# https://m.weibo.cn/profile/{0}.format(uid) url构造里面找最为靠前的uid参数
# https://m.weibo.cn/p/index?containerid=231051_-_followers_-_5692692520 关注者信息 id中uid需要寻找，其他参数均为固定。
# https://m.weibo.cn/p/index?containerid=231051_-_fans_-_5692692520 粉丝信息
    
def get_fans(page,uid):   #uid网页构造变换的关键
    base_url = 'https://m.weibo.cn/api/container/getIndex?'  
    headers = {  
    'Host': 'm.weibo.cn',   
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  
    'X-Requested-With': 'XMLHttpRequest'}  
    params = {  
        'type': 'uid',  
        'containerid': '231051_-_followers_-_{0}'.format(uid),
        'page': page  
    }  
    url = base_url + urlencode(params) 
    try:  
        response = requests.get(url, headers=headers)  
        if response.status_code == 200:  
            return response.json()
    except requests.ConnectionError as e:  
        print('Error', e.args)   
        
def count_all(json):
    if json:
        total = json.get('data').get('cardlistInfo').get('total') #寻找数据中的关注量的总数
        
    return total

def parse_fans(json):  
    if json:  
        items = json.get('data').get('cards') #拆分字典
        try :     #try语句，解决list溢出
            card_group = items[-1].get('card_group')#最后一组开始
        except IndexError:
            try:
                card_group = items[1].get('card_group')#字典中1位的数组内容
            except IndexError:
                try:
                    card_group = items[0].get('card_group')#字典中0位的数组内容 ,这里缘于其构造问题，得先看item[1],再看itme[0],视具体情况而定，也可以-1
                except IndexError:
                    pass
        weibo = {}
        i = 0
        try:
            while card_group[i].get('desc2'):
                name = card_group[i].get('user').get('screen_name')
                weibo['name'] = name
                weibo['fans_count'] = card_group[i].get('desc2')#粉丝数量
                weibo['fans_id'] = card_group[i].get('user').get('id')#粉丝自己的uid                
                i +=1
                yield weibo
        except:
            pass
        
def parse_person(uid):  
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283{0}_-_INFO&title=基本资料&luicode=10000011&lfid=230283{0}'.format(uid)
    try:  
        response = requests.get(url, headers=headers)  
        if response.status_code == 200:  
            content =  response.json()
    except requests.ConnectionError as e:  
        print('Error', e.args)
        
    person = {}

    try:
        items = content.get('data').get('cards') #拆分字典，是为数组
        card_group = items[0].get('card_group') #分类
        person["introduction"] = card_group[2].get('item_content')  #简介
    #    person['name'] = card_group[1].get('item_content')   #昵称
    except:
        person['introduction'] = '无'
        person['gender'] = '无'
        person['zone'] = '无'
        return person
    
    try:
        items = content.get('data').get('cards') #拆分字典，是为数组
        card_group = items[1].get('card_group') #分类
    except:
        person['gender'] = '无'
        person['zone'] = '无'
        return person
    try:
        person['gender'] = card_group[1].get('item_content') #性别
        if (person['gender'] != '男') and (person['gender'] != '女'):
            person['zone'] = person['gender']
            person['gender'] = '无'
        else:
            person['zone'] = card_group[2].get('item_content')#所在地
    except IndexError:
        person['gender'] = '无'
        
    return person 

def main():
    uid = 1660963912 #uid网页构造变换的关键
    json = get_fans(1,uid)
    count = count_all(json)
    print("总共有{0}位关注者".format(count))
    num = int(count/20 + 1) #每一页粉丝爬取20个
    for page in range(1, num):  
        json = get_fans(page,uid)  
        weibos = parse_fans(json)  
        for weibo in weibos:  
            person = parse_person(weibo['fans_id'])
            with open('微博关注者信息.csv','a') as f: #csv文件
                zone = csv.writer(f)
                zone.writerows([[weibo['name'],weibo['fans_count'],person['gender'],person['zone'],person['introduction']]])
                #微博名字，粉丝数量，性别，所在地,微博个人简介   
    print("爬取成功！")#因为大多数博主关注者数量灌水，实际爬取会少很多数量
    
if __name__ == '__main__': 
    main()
