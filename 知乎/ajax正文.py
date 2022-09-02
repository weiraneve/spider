import requests,json
from pyquery import PyQuery as pq#用来去标签

for page in range(0,10,5):#offset 步长为5
    url = 'https://www.zhihu.com/api/v4/questions/389005632/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={0}&platform=desktop&sort_by=default'.format(page)
    #ajax类型爬取，得仔细找偏移量
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    response = requests.get(url, headers = headers).json()#变为json格式
    data = response.get('data')#字典‘data’为列表，需要遍历，然后再运用字典的方法
    for item in data:
        with open('txt.txt','a') as f:
            f.write(pq(item['content']).text())#需要正文
        
