import re
from pdlearn import mydriver
import sys
import time

def get_dd():
    while True:
        dname = input('请输入正确的学习强国帐号(钉钉手机号)：')
        ret = re.match(r"^1[3-9]\d{9}$", dname)
        if ret:
            pwd = input("请输入学习强国密码：")
            break
    return dname, pwd


def dd_login_status(uname, has_dd=False):
    while True:
        if has_dd:
            dname, pwd = load_dingding("./user/{}/dingding".format(uname))
            print("读取用户信息成功")
        else:
            dname, pwd = get_dd()
        driver_login = mydriver.Mydriver(noimg=False,nohead=False) #添加nohead=True
        login_status = driver_login.dd_login(dname, pwd)
        time.sleep(15)
        if login_status:
            save_dingding("./user/{}/dingding".format(uname), dname, pwd)
            cookies = driver_login.get_cookies()
            # driver_login.quit()
            break
    return driver_login, cookies


def save_dingding(user_path, dname, pwd):
    with open(user_path, "w", encoding="utf8") as fp:
        fp.write(dname + "," + pwd)


def load_dingding(user_path):
    with open(user_path, "r", encoding="utf8") as fp:
        try:
            dname, pwd = fp.read().split(",")
            return dname, pwd
        except:
            print("钉钉记录文件损坏，错误代码3程序退出")
            sys.exit(3)

