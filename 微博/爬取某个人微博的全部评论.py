#对于微博的xhr型网页爬取，点赞评论等内容
from urllib.parse import urlencode  
import requests,re,csv,time,json,random
from pyquery import PyQuery as pq
#https://m.weibo.cn/u/2377356574?uid=2377356574&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D浴中奇思
#使用上述微博页面才好爬

with open('ck.txt','r') as f :    #这里的微博运用selenium接管，写入cookies
    cookies = f.read()  #读取cookies    
    cookies = json.loads(cookies)
    
def get_comment(url,id_): #从评论中获取信息
    time.sleep(5) #如果可以的话可以调试下这个暂停时间，微博的话，1秒肯定不行
    response = requests.get(url,cookies = cookies) #也可以试着使用IP池  
    comment = response.json() 
    #微博评论现在的构造自有玄机可参考下：https://www.jianshu.com/p/8dc04794e35f
    if comment['ok'] == 1: 
        max_id = comment["data"]["max_id"] #一页有20条评论
        next_url = "https://m.weibo.cn/comments/hotflow?id={0}&mid={0}&max_id={1}&max_id_type=0".format(id_,max_id)
        for comment_data in comment["data"]["data"]: #字典data中data嵌套
            text = comment_data["text"] #for循环寻找正文“text”
            p = re.compile(r'(<span.*>.*</span>)*(<a.*>.*</ a>)?')  #通过正则，去掉其中夹杂的标签。
            text = p.sub(r'', text)
            like_num = comment_data['like_count'] #评论点赞数
            creat_time = comment_data['created_at'] #评论创建时间
            #具体化评论者性别
            if comment_data['user']['gender'] =='f': 
                gender = "女"
            elif comment_data['user']['gender'] =='m':
                gender = "男"
            else :
                gender = "平台"
    #         comment_dict["id"] = comment_data['user']['id'] #评论者个人微博网址id
            comment_dict = {}
            comment_dict["评论正文"] = text
            comment_dict["评论点赞"] = like_num
            comment_dict["评论时间"] = creat_time
            comment_dict["名字"] = comment_data['user']['screen_name'] #评论者名字
            comment_dict["性别"] = gender #评论者性别
            comment_dict["签名"] = comment_data['user']['description'] #评论者个性签名
            comment_dict["粉丝数"] = comment_data['user']['followers_count'] #评论者粉丝数
            comment_dict["关注数"] = comment_data['user']['follow_count'] #评论者关注数
            #其中每一条评论之下还可能有其他评论，这也是有信息可以爬取的，具体看json数据信息。
            # json信息还含有不少其他信息，这里不一一列举了。
            with open('{0}微博评论信息.csv'.format(id_),'a') as f: #csv文件
                zone = csv.writer(f)
                zone.writerows([[comment_dict['评论正文'],comment_dict['评论点赞'],comment_dict['评论时间'],comment_dict['名字'],comment_dict['性别'],comment_dict['签名'],comment_dict['性别'],comment_dict['粉丝数'],comment_dict['关注数']]])   
    try: #这里的bug无法优雅地解决，只能用try语句试试
        get_comment(next_url,id_) #递归解决
    except:
        pass
#     get_comment(next_url,id_) #递归
    
def get_page(page):  #爬取个人微博主页
    base_url = 'https://m.weibo.cn/api/container/getIndex?'
    params = {  
        'type': 'uid',  
        'value': '1749127163',  #value 与containerid是变化的关键,在那个xhr里面找
        'containerid': '1076031749127163',  #containerid要xhr里面不变动的数值
        'page': page  
    }  
    url = base_url + urlencode(params) 
    try:  
        response = requests.get(url)  
        if response.status_code == 200:  
            return response.json()
    except requests.ConnectionError as e:  
        print('Error', e.args)          

def parse_page(json):  #从个人主页超文本中获取信息
    if json:  
        items = json.get('data').get('cards')  
        for item in items:  
            item = item.get('mblog')  
            if item:
                weibo = {}   
                weibo['微博id'] = item.get('id')#爬取具体微博的id
                yield weibo
            
if __name__ == '__main__':  
    for page in range(1,3):  
        json = get_page(page)  #爬取个人主页
        results = parse_page(json)  #从个人主页中爬取到具体微博的id集合
        for result in results:  #遍历
            id_ = result['微博id'] #对应每一条具体评论的id
            with open('{0}微博评论信息.csv'.format(id_),'a') as f: 
                zone = csv.writer(f)
                zone.writerows([["评论正文","评论点赞","评论时间","名字","性别","签名","性别","粉丝数","关注数"]])
            # 先给csv第一行赋予属性
            origin_url = "https://m.weibo.cn/comments/hotflow?id={0}&mid={0}&max_id_type=0".format(id_)
            get_comment(origin_url,id_)

