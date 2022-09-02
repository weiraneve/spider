#对于微博的xhr型网页爬取，点赞评论等内容
from urllib.parse import urlencode  
import requests  
from pyquery import PyQuery as pq
#https://m.weibo.cn/u/2377356574?uid=2377356574&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D浴中奇思
#使用上述微博页面才好爬
base_url = 'https://m.weibo.cn/api/container/getIndex?'
def get_page(page):  
    params = {  
        'type': 'uid',  
        'value': '2103197132',  #value 与containerid是变化的关键,在那个xhr里面找
        'containerid': '1076032103197132',  #containerid要xhr里面不变动的数值
        'page': page  
    }  
    url = base_url + urlencode(params) 

    try:  
        response = requests.get(url)
        if response.status_code == 200:  
            return response.json()
    except requests.ConnectionError as e:  
        print('Error', e.args)          

def parse_page(json):  
    if json:  
        items = json.get('data').get('cards')  
        for item in items:  
            item = item.get('mblog')  
            if item:
                weibo = {}   
                weibo['正文'] = pq(item.get('text')).text()#爬取正文 ，pq库为了去掉正文的标签
                weibo['点赞数  '] = item.get('attitudes_count')#爬取点赞数  
                weibo['评论'] = item.get('comments_count')  #爬取评论
                weibo['转发数'] = item.get('reposts_count')  #爬取转发数
                weibo['创建时间'] = item.get('created_at')  #爬取创建时间
                yield weibo
            
if __name__ == '__main__':  
    for page in range(1,11):  
        json = get_page(page)  
        results = parse_page(json)  
        for result in results:  
#             print(reuslt)
            with open("100.txt",'a') as f:
                f.write(str(result))
