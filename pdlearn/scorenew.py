from pdlearn import mydriver
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_score(driver):
    try:
        total = driver.find_element_by_css_selector('div.my-points-block')
        total = total.text.splitlines()
        myscores = {'总积分': total[1]}
        each = driver.find_elements_by_css_selector('div.my-points-card-text')
        name = ['登陆', '阅读文章', '视听学习', '文章时长', '视频时长']
        for i in range(len(name)):
            myscores.update({name[i]: int(each[i].text[0])})
        for i in range(len(name)):
            myscores.update({name[i]+'目标': int(each[i].text[3])})
        return myscores
    except:
        # driver.close()
        print("=" * 120)
        print("get_score获取失败")
        print("=" * 120)
        raise
def get_diandian(driver):
    try:
        total = driver.find_element_by_css_selector('div.my-points-block')
        total = total.text.splitlines()
        mydian = {'点点通': total[1]}
        each = driver.find_elements_by_css_selector('div.my-points-card-text')
        name = ['有效浏览', '有效视听']
        for i in range(len(name)):
            mydian.update({name[i]: int(each[i].text[0]) * 6})
        for i in range(len(name)):
            mydian.update({name[i]+'目标': int(each[i].text[3]) * 6})
        return mydian
    except:
        print("=" * 120)
        print("get_diandian获取失败")
        print("=" * 120)
        raise

if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/loukuofeng/PycharmProjects/xuexi/chromedriver')
    print("正在打开二维码登陆界面,请稍后")
    # 直接取二维码，不打开登陆界面
    url = 'https://oapi.dingtalk.com/connect/qrconnect?appid=dingoankubyrfkttorhpou&response_type=code&scope=snsapi_login&redirect_uri=https://pc-api.xuexi.cn/open/api/sns/callback'
    driver.get(url)
    WebDriverWait(driver, 270).until(EC.title_is(u"我的学习"))
    js = " window.open('https://pc.xuexi.cn/points/my-points.html')"
    # driver.go_js(js)
    driver.execute_script(js)
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    WebDriverWait(driver, 270).until(EC.title_is(u"我的积分"))
    time.sleep(10)
    myscores = get_score(driver)
    print(myscores)
    driver.get('https://pc.xuexi.cn/points/ptp.html')
    WebDriverWait(driver, 270).until(EC.title_is(u"我的点点通"))
    # driver.find_element_by_css_selector('button.ant-btn.ant-btn-primary').click()
    time.sleep(10)
    mydian = get_diandian(driver)
    print(mydian)
    myscores.update(mydian)
    driver.switch_to.window(handles[0])