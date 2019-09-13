
from selenium import webdriver
import time
from pdlearn import get_links
import random
import requests
from requests.cookies import RequestsCookieJar
import json

LOGIN_LINK = 'https://pc.xuexi.cn/points/login.html'#登录url
HOME_PAGE = 'https://www.xuexi.cn/'#官方网站url
#使用插件chrimedriver.exe
options = webdriver.ChromeOptions()
options.add_argument('--mute-audio')
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 绕过js检测
browser = webdriver.Chrome(executable_path=r'./chromedriver',options=options)#这个地方的插件需要对照自己的谷歌版本去下载
'''
谷歌版本号查询地址:chrome://version
查询谷歌和chromedriver对应的版本:https://blog.csdn.net/huilan_same/article/details/51896672
chromedriver下载地址:http://chromedriver.storage.googleapis.com/index.html

'''
def login_simulation():
    browser.get(LOGIN_LINK)
    browser.maximize_window()
    browser.execute_script("var q=document.documentElement.scrollTop=800")
    time.sleep(30)
    browser.get(HOME_PAGE)
    cookies = browser.get_cookies()
    print("模拟登录完毕\n")
    return cookies

def watch_videos():
    """观看视频"""
    links = get_links.get_video_links()
    random.shuffle(links)
    i = 0
    for link in random.sample(links, 35):
        browser.get(link)
        browser.execute_script("var q=document.documentElement.scrollTop=500")
        time.sleep(random.randint(60, 75))
        i += 1
        print(i,time.ctime(time.time()),browser.title)
    print("播放视频完毕\n")
def watch_videos1(cookies):
    """观看视频"""
    cookieprint(cookies)
    #links = get_links.get_video_links()
    videosbrower = webdriver.Chrome(executable_path=r'./chromedriver',options=options)
    videosbrower.get(HOME_PAGE)
    print("aaaaaa")
    cookies2 = videosbrower.get_cookies()
    cookieprint(cookies2)

    #videosbrower.delete_all_cookies()
    print("bbbbbb")
    for cookie in cookies:
        videosbrower.add_cookie(cookie_dict=cookie)#{k: cookie[k] for k in cookie.keys()})
    print("AAAAAAAAAA")
    cookieprint(videosbrower.get_cookies())
    videosbrower.get(HOME_PAGE)

def cookieprint(cookies):
    i = 0
    for cookie in cookies:
        i += 1
        print(i,cookie)#{k: cookie[k] for k in cookie.keys()})

def read_articles():
    """阅读文章"""
    j = 0
    links = get_links.get_article_links()
    random.shuffle(links)
    for link in random.sample(links, 20):
        browser.get(link)
        for i in range(0, 2000, 100):
            js_code = "var q=document.documentElement.scrollTop=" + str(i)
            browser.execute_script(js_code)
            time.sleep(1)
        for i in range(2000, 0, -100):
            js_code = "var q=document.documentElement.scrollTop=" + str(i)
            browser.execute_script(js_code)
            time.sleep(1)
        #time.sleep(20)
        j += 1
        print(j, browser.title)
    print("阅读文章完毕\n")

def get_score(cookies):
    try:
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        total = requests.get("https://pc-api.xuexi.cn/open/api/score/get", cookies=jar).content.decode("utf8")
        total = int(json.loads(total, encoding="utf8")["data"]["score"])
        each = requests.get("https://pc-api.xuexi.cn/open/api/score/today/queryrate", cookies=jar).content.decode(
            "utf8")
        each = json.loads(each, encoding="utf8")["data"]["dayScoreDtos"]
        each = [int(i["currentScore"]) for i in each if i["ruleId"] in [1, 2, 9, 1002, 1003]]
        return total, each
    except:
        print("=" * 120)
        print("get_scores获取失败")
        print("=" * 120)
        raise

if __name__ == '__main__':
    cookies = login_simulation()  # 模拟登录
    #read_articles()     # 阅读文章
    #watch_videos()      # 观看视频
    watch_videos1(cookies)
    total,each = get_score(cookies)        # 获得今日积分
    print("当前学习总积分：" + str(total))
    print("阅读文章:{}/6,观看视频:{}/6,登陆:{}/1,文章时长:{}/6,视频时长:{}/6".format(*each))
    browser.quit()