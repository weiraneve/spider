from selenium import webdriver as web
from requests import get, post
import json
import time
from os import path

def get_g_tk(p_skey):
    hashes = 5381
    for letter in p_skey:
        hashes += (hashes << 5) + ord(letter)
    return hashes & 0x7fffffff

def del_dt(tid):
    data = {
        "hostuin": qq,
        "tid": tid,
        "t1_source": 1,
        "code_version": 1,
        "format": "fs",
        "qzreferrer": r"https://user.qzone.qq.com/%s/infocenter" % qq
    }
    params = {
        "g_tk": g_tk
    }
    post(url="https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_delete_v6",
                       params=params, data=data, cookies=cookie
                       )
def get_dt():
    params = {
        "uin": qq,
        "inCharset": "utf-8",
        "outCharset": "utf-8",
        "hostUin": qq,
        "notice": "0",
        "sort": "0",
        "pos": "0",
        "num": "20",
        "cgi_host": "https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
        "code_version": "1",
        "format": "jsonp",
        "need_private_comment": "1",
        "g_tk": g_tk
    }
    req = get("https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6", params=params, cookies=cookie)
    text = req.content.decode("utf-8")
    text = text.replace("_Callback(", "")
    text = text[:-2]
    js = json.loads(text)
    msg_list = js["msglist"]
    if msg_list is None:
        return False, []
    m_list = []
    for msg in msg_list:
        tid = msg["tid"]
        content = msg["content"]
        localtime = time.localtime(msg["created_time"])
        t = time.strftime("%Y/%m/%d %H:%M", localtime)
        m_list.append((tid, t, content))
    return True, m_list

def run():
    global g_tk, cookie, qq
    driver =  webdriver.Chrome()
    driver.get("https://qzone.qq.com/")
    input("完成登录后按回车继续...")
    cookies = driver.get_cookies()
    cookie = {}
    for c in cookies:
        name = c["name"]
        value = c["value"]
        cookie[name] = str(value)
    p_skey = cookie["p_skey"]
    qq = cookie["uin"][2:]
    print("你的QQ号：%s" % qq)
    g_tk = get_g_tk(p_skey)
    confirm = False
    while True:
        gt = get_dt()
        if gt[0]:
            msg_list = gt[1]
            for msg in msg_list:
                if not confirm:
                    c = input("已成功获取到说说，确认删除？（输入大写Y确认）：")
                    if c == "Y":
                        confirm = True
                    else:
                        exit()
                print("正在删除说说：%s %s" % (msg[1], msg[2]))
                del_dt(msg[0])
                pass
        else:
            print("说说已清空")
            break
    driver.close()

run()
input("按回车键退出...")

