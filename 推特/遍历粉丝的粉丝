
def fans_to_fans(origin_path):  
    #将这个文件夹里的csv文件遍历，然后在此路径下创建子文件夹以及子文件夹中的粉丝数据csv文件
    name = str(origin_path)
    name = name.split('/')[-1]
    with open('{0}/{1}的粉丝.csv'.format(origin_path,name), 'r') as f: #读取csv
        reader = csv.reader(f)
        count = 0 
        for row in reader:
            count += 1
            if (count != 1): # #不取1
                url_name = row[0]
                url_name = url_name.split("@")[1]
                path = "{0}/{1}".format(origin_path,url_name) #路径文件夹是否存在
                isExists = os.path.exists(path) 
                if not isExists: #不存在则创建文件夹
                    os.mkdir(path) 
                get_fans(url_name,path)
            elif count > max_limit:
                return #大于限制后提前结束

def fans_three(origin_path): #遍历这个根目录文件名路径下的所有子文件夹名字
    result = os.listdir(origin_path) #最初的根文件夹名
    for file_name in result:
        if (file_name[0] == '.') | (file_name[-4:] == '.csv'):
            pass
        else :
            file_name = origin_path + '/' + file_name
            fans_to_fans(file_name)  #调用函数
        
origin_path = "/Users/shanshan/Desktop/python/doublelift1" #根目录文件名
fans_three(origin_path)

