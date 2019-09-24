from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from pdlearn import user_agent
from pdlearn import chaojiying
from PIL import Image
from configparser import ConfigParser
import json
import time
import os
import pytesseract


class Mydriver:

    def __init__(self, noimg=True, nohead=True):
        try:
            self.options = Options()
            if os.path.exists("./chrome/chrome.exe"):  # win
                self.options.binary_location = "./chrome/chrome.exe"
            elif os.path.exists("/opt/google/chrome/chrome"):  # linux
                self.options.binary_location = "/opt/google/chrome/chrome"
            if noimg:
                self.options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            if nohead:
                self.options.add_argument('--headless')
                self.options.add_argument('--disable-extensions')
                self.options.add_argument('--disable-gpu')
                self.options.add_argument('--no-sandbox')
            self.options.add_argument('--mute-audio')  # 关闭声音
            self.options.add_argument('--window-size=400,500')  # 将某个窗口设置为固定大小
            self.options.add_argument('--window-position=800,0')  # 将某个窗口移动到指定的位置
            self.options.add_argument('--log-level=3')  # info(default) = 0,warning = 1,LOG_ERROR = 2,LOG_FATAL = 3

            # 去掉保存密码提示
            self.options.add_experimental_option('prefs', {
                'credentials_enable_service': False,
                'profile': {
                    'password_manager_enabled': False
                }
            })

            self.options.add_argument('--user-agent={}'.format(user_agent.getheaders()))
            self.options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 绕过js检测
            self.webdriver = webdriver
            if os.path.exists("./chrome/chromedriver.exe"):  # win
                self.driver = self.webdriver.Chrome(executable_path="./chrome/chromedriver.exe",
                                                    chrome_options=self.options)
            elif os.path.exists("./chromedriver"):  # linux
                self.driver = self.webdriver.Chrome(executable_path="./chromedriver",
                                                    chrome_options=self.options)
            elif os.path.exists("/usr/lib64/chromium-browser/chromedriver"):  # linux 包安装chromedriver
                self.driver = self.webdriver.Chrome(executable_path="/usr/lib64/chromium-browser/chromedriver",
                                                    chrome_options=self.options)
            elif os.path.exists("/usr/local/bin/chromedriver"):  # linux 包安装chromedriver
                self.driver = self.webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",
                                                    chrome_options=self.options)
            else:
                self.driver = self.webdriver.Chrome(chrome_options=self.options)
        except:
            print("=" * 120)
            print("Mydriver初始化失败")
            print("=" * 120)
            raise

    def login(self):
        print("正在打开二维码登陆界面,请稍后")
        # 直接取二维码，不打开登陆界面
        url = 'https://oapi.dingtalk.com/connect/qrconnect?appid=dingoankubyrfkttorhpou&response_type=code&scope=snsapi_login&redirect_uri=https://pc-api.xuexi.cn/open/api/sns/callback'
        self.driver.get(url)

        '''
        #self.driver.get("https://pc.xuexi.cn/points/login.html")
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("redflagbox"))
        except exceptions.TimeoutException:
            print("网络缓慢，请重试")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("header"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
        try:
            remover = WebDriverWait(self.driver, 30, 0.2).until(
                lambda driver: driver.find_element_by_class_name("footer"))
        except exceptions.TimeoutException:
            print("当前网络缓慢...")
        else:
            self.driver.execute_script('arguments[0].remove()', remover)
            self.driver.execute_script('window.scrollTo(document.body.scrollWidth/2 - 200 , 0)')
        '''
        try:
            WebDriverWait(self.driver, 5).until(EC.title_is(u"二维码登录"))
            self.driver.save_screenshot('./user/screenshot.png')  # 对二维码截个图
            WebDriverWait(self.driver, 270).until(EC.title_is(u"我的学习"))
            cookies = self.get_cookies()
            return cookies
        except:
            print("扫描二维码超时")

    def dd_login(self, d_name, pwd):
        __login_status = False
        self.driver.get(
            "https://login.dingtalk.com/login/index.htm?"
            "goto=https%3A%2F%2Foapi.dingtalk.com%2Fconnect%2Foauth2%2Fsns_authorize"
            "%3Fappid%3Ddingoankubyrfkttorhpou%26response_type%3Dcode%26scope%3Dsnsapi"
            "_login%26redirect_uri%3Dhttps%3A%2F%2Fpc-api.xuexi.cn%2Fopen%2Fapi%2Fsns%2Fcallback"
        )
        time.sleep(1)  # 等待加载网页
        self.driver.find_elements_by_id("mobile")[0].click()
        self.driver.find_element_by_id("mobile").send_keys(d_name)
        self.driver.find_elements_by_id("pwd")[0].click()
        self.driver.find_element_by_id("pwd").send_keys(pwd)
        self.driver.find_element_by_id("loginBtn").click()

        time.sleep(1)  # 等待加载验证码图片
        self.driver.save_screenshot('./user/' + d_name + '.png')  # 网页截图
        element = self.driver.find_element_by_xpath('//div[@class="indentify_content"]/img')  # 找到验证码图片位置
        # print(element.location)  # 打印元素坐标
        # print(element.size)  # 打印元素大小
        left = element.location['x'] * 2  # 获取left数值
        top = element.location['y'] * 2  # 获取top数值
        right = (element.location['x'] + element.size['width']) * 2  # 获取right数值
        bottom = (element.location['y'] + element.size['height']) * 2  # 获取bottom数值
        im = Image.open('./user/' + d_name + '.png')  # 读取图片
        # print((left,top,right,bottom))
        im = im.crop((left, top, right, bottom))  # 截取验证码位置
        im.save('./user/identifyCode.png', 'png')  # 将得到的图片保存在本地
        # time.sleep(100)
        # code = pytesseract.image_to_string(im)
        # print(code)
        '''
        # 开始识别操作
        config = ConfigParser()
        config.read('config.conf', encoding='UTF-8')
        chaoji = chaojiying.Chaojiying_Client(config.get('identifyCode', 'UserName'),
                                              config.get('identifyCode', 'Password'),
                                              config.get('identifyCode', 'SoftID'))  # 用户中心>>软件ID 生成一个替换 96001
        im_identifyCode = open('./user/identifyCode.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        code_str = chaoji.PostPic(im_identifyCode, 1104)  # 识别图片文字并返回(json格式)
        code = code_str['pic_str']
        im.save('./user/' + code + '_identifyCode.png')  # 将得到的图片保存在本地
        # print(code) #1902 验证码类型
        if config.get('identifyCode', 'UseApi') != 'False':
            chaoji = chaojiying.Chaojiying_Client(config.get('identifyCode', 'UserName'),
                                                  config.get('identifyCode', 'Password'),
                                                  config.get('identifyCode', 'SoftID'))  # 用户中心>>软件ID 生成一个替换 96001
            im_identifyCode = open('./user/identifyCode.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
            code_str = chaoji.PostPic(im_identifyCode, 1104)  # 识别图片文字并返回(json格式)
            code = code_str['pic_str']
            im.save('./user/' + code + '_identifyCode.png')  # 将得到的图片保存在本地
            print('验证码识别结果：'+ code)  # 1902 验证码类型
        else:
            print('验证码登录漏洞')
            code = 'v v '
        time.sleep(10)
        '''
        self.driver.find_elements_by_id("identifyCode")[0].click()
        # self.driver.find_element_by_id("identifyCode").send_keys(code)
        # self.driver.find_element_by_id("identifybtn").click()

        try:
            print("登陆中...")
            WebDriverWait(self.driver, 2, 0.1).until(lambda driver: driver.find_element_by_class_name("modal"))
            print(self.driver.find_element_by_class_name("modal").find_elements_by_tag_name("div")[0].text)
            self.driver.quit()
            __login_status = False
        except:
            __login_status = True
        return __login_status

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return cookies

    def set_cookies(self, cookies):
        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            self.driver.add_cookie({k: cookie[k] for k in cookie.keys()})
            # print('set_cookies中', {k: cookie[k] for k in cookie.keys()})
        # print('set_cookies',self.driver.get_cookies())

    def get_url(self, url):
        self.driver.get(url)

    def go_js(self, js):
        self.driver.execute_script(js)

    def get_title(self):
        title = self.driver.title
        return title

    def quit(self):
        self.driver.quit()

    def web_wait(self, s_time, title):
        WebDriverWait(self.driver, s_time).until(EC.title_is(title))

    def in_driver(self):
        driver1 = self.driver
        return driver1
