import time

def get_score(driver):
    try:
        driver.get_url('https://pc.xuexi.cn/points/my-points.html')
        driver.web_wait(270, u"我的积分")
        time.sleep(10)
        driver1 = driver.in_driver()
        total = driver1.find_element_by_css_selector('div.my-points-block')
        total = total.text.splitlines()
        myscores = {'总积分': total[1]}
        each = driver1.find_elements_by_css_selector('div.my-points-card-text')
        name = ['登陆', '阅读文章', '视听学习', '文章时长', '视听学习时长']
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
        driver.get_url('https://pc.xuexi.cn/points/ptp.html')
        driver.web_wait(270, u"我的点点通")
        # driver.find_element_by_css_selector('button.ant-btn.ant-btn-primary').click()
        time.sleep(10)
        driver2 = driver.in_driver()
        total = driver2.find_element_by_css_selector('div.my-points-block')
        total = total.text.splitlines()
        mydian = {'点点通': total[1]}
        each = driver2.find_elements_by_css_selector('div.my-points-card-text')
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

