import requests,csv,json

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
        
def parse_data(html):
    json_data = json.loads(html)['data']
    try:
        for item in json_data:
            comment = {}
            comment['name'] = (item['author']['name'])    # 姓名
            comment['gender'] = (item['author']['gender'])  # 性别
            comment['vote'] = (item['voteup_count'])      # 点赞数
            comment['comment'] = (item['comment_count'])     # 评论数
            #comment['person'] = (item['author']['url'])     # 个人主页
            #comment['link'] = (item['url'])               # 回答链接
            yield comment

    except Exception as e:
        print(comment)
        print(e)

def save_data(comment):
    '''
    功能：将comments中的信息输出到文件中/或数据库中。
    参数：comments 将要保存的数据  
    '''
    filename = 'data.csv'
    comment['vote'] = '点赞数：' + str(comment['vote'])
    comment['comment'] = '评论数' + str(comment['comment'])
    #comment['link'] = '回答链接' + str(comment['link'])
    #comment['person'] = '个人主页' + str(comment['person'])
    if comment['gender'] == int(1):
        comment['gender'] = '匿名用户'
    elif comment['gender'] == int(0):
            comment['gender'] = '女'
    elif comment['gender'] == int(-1):
            comment['gender'] = '男'
    with open(filename,'a') as f:
        zone = csv.writer(f)
        zone.writerows([[comment['name'],comment['gender'],comment['vote'],comment['comment']]])

def main():
    page = 0
    key = 47832005 #自己寻找question后的数字
    url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={1}&platform=desktop&sort_by=default'.format(key,page)
    # get total cmts number
    html = get_data(url)
    totals = json.loads(html)['paging']['totals']
    print('总共有{0}条回答'.format(totals))
    print('---'*10)
    while(page < totals):
        url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={1}&platform=desktop&sort_by=default'.format(key,page)
        html = get_data(url)
        comments = parse_data(html)
        for comment in comments:
            save_data(comment)
        page += 5
        
if __name__ == '__main__':
    main()
    print("完成！！")
