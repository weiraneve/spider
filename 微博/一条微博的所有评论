import requests,re,csv,time,json

with open('ck.txt','r') as f :    #这里的微博运用selenium接管，写入cookies
    cookies = f.read()  #读取cookies    
    cookies = json.loads(cookies)

def get_comment(url):
    response = requests.get(url,cookies = cookies)  
    comment = response.json() 
    #微博评论现在的构造自有玄机可参考下：https://www.jianshu.com/p/8dc04794e35f
    if comment['ok'] == 1: 
        max_id = comment["data"]["max_id"] #一页有20条评论
        next_url = "https://m.weibo.cn/comments/hotflow?id=4588610269743209&mid=4588610269743209&max_id={0}&max_id_type=0".format(max_id)
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
            with open('微博评论信息.csv','a') as f: #csv文件
                zone = csv.writer(f)
                zone.writerows([[comment_dict['评论正文'],comment_dict['评论点赞'],comment_dict['评论时间'],comment_dict['名字'],comment_dict['性别'],comment_dict['签名'],comment_dict['性别'],comment_dict['粉丝数'],comment_dict['关注数']]])   

    get_comment(next_url)

# next_url = "https://m.weibo.cn/comments/hotflow?id=4588610269743209&mid=4588610269743209&max_id={0}&max_id_type=0".format(max_id)

if __name__ == '__main__':
    with open('微博评论信息.csv','a') as f: # 先给第一行赋予属性
        zone = csv.writer(f)
        zone.writerows([["评论正文","评论点赞","评论时间","名字","性别","签名","性别","粉丝数","关注数"]])
    origin_url = "https://m.weibo.cn/comments/hotflow?id=4588610269743209&mid=4588610269743209&max_id_type=0"
    get_comment(origin_url)
    
