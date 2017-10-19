#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import re

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote, unquote

cc98_cookie = {"aspsky": "username=baoku511&usercookies=3&userid=558481&useranony=&userhidden=2&password=4197d53015e2bb6a"}
nhd_cookie_str = "c_secure_uid=OTgyMDI%3D; c_secure_pass=c3b92444fb78914c533314e4348f7519; c_secure_ssl=bm9wZQ%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_login=bm9wZQ%3D%3D; c_lang_folder=en"

UALIST = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
]

def cc98_bonous():
    print('cc98_bonous----in----')
    session = requests.Session()
    session.headers.update({'User-Agent': random.choice(UALIST)})
    session.cookies.update(cc98_cookie)
    response = session.get(url='http://www.cc98.org/usermanager.asp')
    html_doc = str(response.text)
    bonous = html_doc.split('用户财富： ')[1].split('<')[0]
    print('用户财富： ' + bonous)
    print('cc98_bonous----out----')
    return bonous

def cc98_login_check():
    print('cc98_login_check----in----')

    bonous_before = cc98_bonous()

    session_check = requests.Session()
    session_check.headers.update({'User-Agent': random.choice(UALIST)})
    session_check.cookies.update(cc98_cookie)
    response_check = session_check.get(url="http://www.cc98.org/signin.asp")
    # print(response_check.text)
    response_check = session_check.post(url="http://www.cc98.org/signin.asp?action=save", data="Expression=face7.gif&content=%E7%AD%BE%E5%88%B0%E7%AD%BE%E5%88%B0", headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})

    bonous_after = cc98_bonous()

    try:
        if float(bonous_before.replace(',', '')) < float(bonous_after.replace(',', '')):
            print('CC98签到成功')
        else:
            print('CC98已签到')
    except:
        print('bonous string to int error')

    # if "/dispbbs.asp?boardid=326&id=4635712" in response_check.text:
    #     print('签到成功')
    # else:
    #     print('你今天已经签到过了，请明天再来~')
    print('cc98_login_check----out----')

def setcookie(session, cookiestring):
    cookie = {}
    if cookiestring is not None:
        for onecookiestring in cookiestring.split(";"):
            tmp = onecookiestring.split("=")
            if len(tmp)!=2:
                continue
            a, b = tmp
            a = quote(unquote(a).strip())
            cookie.update({a: b})
        session.cookies.update(cookie)

def nhd_bonous():
    print('nhd_bonous----in----')
    session = requests.Session()
    session.headers.update({'User-Agent': random.choice(UALIST)})
    setcookie(session, nhd_cookie_str)
    response = session.get(url='http://www.nexushd.org/mybonus.php')
    html_doc = str(response.text)
    bonous = html_doc.split("""[<a href="mybonus.php">Use</a>]:""")[1].split("<",2)[0].strip()
    print('魔力值： ' + bonous)
    print('nhd_bonous----out----')
    return bonous

def nhd_login_check():
    print('nhd_login_check----in----')

    bonous_before = nhd_bonous()

    session_check = requests.Session()
    session_check.headers.update({'User-Agent': random.choice(UALIST)})
    setcookie(session_check, nhd_cookie_str)
    response_check = session_check.post("http://www.nexushd.org/signin.php", data="action=post&content=auto+reply...+%5Bem4%5D+", headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})

    bonous_after = nhd_bonous()

    try:
        if float(bonous_before.replace(',', '')) < float(bonous_after.replace(',', '')):
            print('NHD签到成功')
        else:
            print('NHD已签到')
    except:
        print('bonous string to int error')
    print('nhd_login_check----out----')

if __name__ == '__main__':
    print('auto_login_check----in----')
    cc98_login_check()
    nhd_login_check()
    print('auto_login_check----out----')
