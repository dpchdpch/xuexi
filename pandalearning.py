import time
from sys import argv
import random

from pdlearn import version
from pdlearn import user
from pdlearn import dingding
from pdlearn import mydriver
from pdlearn import score
from pdlearn import scorenew
from pdlearn import threads
from pdlearn import get_links


def user_flag(dd_status, uname):
    if dd_status:
        cookies = dingding.dd_login_status(uname, has_dd=True)
    else:
        if (input("是否保存钉钉帐户密码，保存后可后免登陆学习(Y/N) ")) not in ["y", "Y"]:
            driver_login = mydriver.Mydriver(nohead=False)
            cookies = driver_login.login()
            driver_login.quit()
        else:
            cookies = dingding.dd_login_status(uname)
    '''
    a_log = user.get_a_log(uname)
    v_log = user.get_v_log(uname)
    '''
    return cookies


def get_argv():
    nohead = True
    lock = False
    stime = False
    if len(argv) > 2:
        if argv[2] == "hidden":
            nohead = True
        elif argv[2] == "show":
            nohead = False
    if len(argv) > 3:
        if argv[3] == "single":
            lock = True
        elif argv[3] == "multithread":
            lock = False
    if len(argv) > 4:
        if argv[4].isdigit():
            stime = argv[4]
    return nohead, lock, stime


def show_score(cookies):
    myscores = score.get_score(cookies)
    print("当前学习总积分：{}，今日积分：{}".format(str(myscores['总积分']), str(myscores['今日积分'])))
    print("阅读文章:{}/{},视听学习:{}/{},登陆:{}/{},文章时长:{}/{},视频时长:{}/{}".format(
        myscores['阅读文章'], myscores['阅读文章目标'],
        myscores['视听学习'], myscores['视听学习目标'],
        myscores['登录'], myscores['登录目标'],
        myscores['文章时长'], myscores['文章时长目标'],
        myscores['视听学习时长'], myscores['视听学习时长目标']
        ))
    mydian = score.get_diandian(cookies)
    print("当前点点通：{}，今日点点通：{}".format(str(mydian['点点通']), str(mydian['今日点点通'])))
    print("有效浏览:{}/{},有效视听:{}/{},挑战答题:{}/{}".format(
        mydian['有效浏览'], mydian['有效浏览目标'],
        mydian['有效视听'], mydian['有效视听目标'],
        mydian['挑战答题'], mydian['挑战答题目标']
        ))
    myscores.update(mydian)
    return myscores

def show_scorenew(driver):
    myscores = scorenew.get_score(driver)
    print("当前学习总积分：{}，今日积分：{}".format(str(myscores['总积分']), str(myscores['今日积分'])))
    print("阅读文章:{}/{},视听学习:{}/{},登陆:{}/{},文章时长:{}/{},视频时长:{}/{}".format(
        myscores['阅读文章'], myscores['阅读文章目标'],
        myscores['视听学习'], myscores['视听学习目标'],
        myscores['登录'], myscores['登录目标'],
        myscores['文章时长'], myscores['文章时长目标'],
        myscores['视听学习时长'], myscores['视听学习时长目标']
        ))
    mydian = scorenew.get_diandian(driver)
    print("当前点点通：{}，今日点点通：{}".format(str(mydian['点点通']), str(mydian['今日点点通'])))
    print("有效浏览:{}/{},有效视听:{}/{}".format(
        mydian['有效浏览'], mydian['有效浏览目标'],
        mydian['有效视听'], mydian['有效视听目标']
        ))
    myscores.update(mydian)
    return myscores

def article(driver_article, a_log, myscores):
    # if each[0] < 6 or each[3] < 8:
    # if deach[0] < 2:
    if myscores['有效浏览'] < myscores['有效浏览目标'] or myscores['文章时长'] < myscores['文章时长目标'] or myscores['阅读文章'] < myscores['阅读文章目标']:
        # driver_article = mydriver.Mydriver(nohead=nohead)
        # driver_article.get_url("https://www.xuexi.cn/notFound.html")
        # driver_article.set_cookies(cookies)
        links = get_links.get_article_links()
        try_count = 0
        lifetime = 0
        while True:
            # if each[0] < 6 and try_count < 10:
            # if deach[0] < 2 and try_count < 20:
            if myscores['有效浏览'] < myscores['有效浏览目标'] or myscores['阅读文章'] < myscores['阅读文章目标'] and try_count < 10:
                # a_num = 6 - each[0]
                # a_num = 20 - deach[0]*10-deach[3]%10 # 检查点点通还差多少条
                # 检查点点通还差多少条
                # a_num_total = min(myscores['有效浏览目标'] - myscores['有效浏览'], 12)
                # a_num = min(random.randint(8, 12), a_num_total)
                a_num = min(myscores['有效浏览目标'] - myscores['有效浏览'], 12)
                #  print(a_num)

                for i in range(a_log, a_log + a_num):
                    driver_article.get_url(links[i])
                    print(i, driver_article.get_title())
                    time.sleep(random.randint(2, 5))
                    # 学习时长
                    # t = random.randint(30, 40)
                    t = (myscores['文章时长目标'] - myscores['文章时长']) * 2 * 60 // a_num  # a_num_total
                    if t < 16:
                        t = random.randint(10, 15)
                    else:
                        t = random.randint(t-5, t+5)
                    lifetime += t
                    # print("时长是：{}".format(t))
                    for j in range(t):
                        if random.random() > 0.5:
                            driver_article.go_js('window.scrollTo(0, (document.body.scrollHeight-1000)/{}*{})'.format(t, j))
                        print("\r文章学习中，文章剩余{}篇,本篇时长{}秒，剩余时间{}秒".format(a_log + a_num - i, t, t - j-1), end="")
                        time.sleep(1)
                    print('')  # lou
                    # driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                myscores.update(show_scorenew(driver_article))
                #if each[0] >= 6:
                # if deach[0] >= 2:
                '''
                if myscores['有效浏览'] >= numtarget and myscores['阅读文章'] >= myscores['阅读文章目标']:
                    print("检测到文章数量分数已满,退出学习")
                    break
                '''
                a_log += a_num
            else:
                with open("./user/{}/a_log".format(myscores['userId']), "w", encoding="utf8") as fp:
                    fp.write(str(a_log))
                print("检测到文章数量分数已满,退出学习")
                break

        try_count = 0
        while True:
            if myscores['文章时长'] < myscores['文章时长目标'] and try_count < 10:
                num_time = 60
                driver_article.get_url(links[a_log-1])
                time.sleep(random.randint(2, 5))
                remaining = (myscores['文章时长目标'] - myscores['文章时长']) * 2 * num_time
                print("剩下时长是：{}".format(remaining))
                lifetime += remaining
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_article.go_js(
                            'window.scrollTo(0, (document.body.scrollHeight-800)/{}*{})'.format(remaining, i))
                    print("\r文章时长学习中，文章总时长剩余{}秒".format(remaining - i - 1), end="")
                    time.sleep(1)
                    '''
                    if i % (120) == 0 and i != remaining:
                        total, each, dtotal, deach, myscores = show_score(driver_article.get_cookies())
                        if myscores['文章时长'] >= timetarget:
                            print("检测到文章时长分数已满,退出学习")
                            break
                    '''
                print('')
                # driver_article.go_js('window.scrollTo(0, document.body.scrollHeight)')
                myscores.update(show_scorenew(driver_article))
            else:
                print("检测到文章时长分数已满,退出学习")
                break

        if try_count < 10:
            print("文章学习完成")
        else:
            print("文章学习出现异常，请检查用户名下a_log文件记录数")
        # driver_article.quit()
        print("学习文章共用时长：{}".format(lifetime))
    else:
        print("文章之前学完了")


def video(driver_video, v_log, myscores):
    # if each[1] < 6 or each[4] < 10:
    # if deach[1] < 2:
    if myscores['有效视听'] < myscores['有效视听目标'] or myscores['视听学习时长'] < myscores['视听学习时长目标'] or myscores['视听学习'] < myscores['视听学习目标']:
        # driver_video = mydriver.Mydriver(nohead=nohead)
        # driver_video.get_url("https://www.xuexi.cn/notFound.html")
        # driver_video.set_cookies(cookies)
        links = get_links.get_video_links()
        try_count = 0
        lifetime = 0
        while True:
            # if each[1] < 6 and try_count < 10:
            # if deach[1] < 2 and try_count < 20:
            if myscores['有效视听'] < myscores['有效视听目标'] or myscores['视听学习'] < myscores['视听学习目标'] and try_count < 10:
                # v_num = 6 - each[1]
                # v_num = 20 - deach[1]*10-deach[4]%10 # 检查点点通还差多少条
                # 检查点点通还差多少条
                # v_num_total = min(myscores['有效视听目标'] - myscores['有效视听'], 12)
                # v_num = min(random.randint(8, 12), v_num_total)
                v_num = min(myscores['有效视听目标'] - myscores['有效视听'], 12)
                for i in range(v_log, v_log + v_num):
                    driver_video.get_url(links[i])
                    print(i, driver_video.get_title())
                    time.sleep(random.randint(2, 5))
                    # 学习时长
                    # t = random.randint(45, 60)
                    t = (myscores['视听学习时长目标'] - myscores['视听学习时长']) * 3 * 60 // v_num  # v_num_total
                    if t < 16:
                        t = random.randint(10, 15)
                    else:
                        t = random.randint(t-5, t+5)
                    t = random.randint(t - 10, t + 10)
                    # print("时长是：{}".format(t))
                    lifetime += t
                    for j in range(t):
                        if random.random() > 0.5:
                            driver_video.go_js('window.scrollTo(0, (document.body.scrollHeight-800)/{}*{})'.format(t, j))
                        print("\r视频学习中，视频剩余{}个,本次时长{}，剩余时间{}秒".format(v_log + v_num - i, t, t - j-1), end="")
                        time.sleep(1)
                    print('') # lou
                    # driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                myscores.update(show_scorenew(driver_video))
                # if each[1] >= 6:
                # if deach[1] >= 2:
                '''
                if myscores['有效视听'] >= myscores['有效视听目标'] and myscores['视听学习'] >= myscores['视听学习目标']:
                    print("检测到视频数量分数已满,退出学习")
                    break
                '''
                v_log += v_num
            else:
                with open("./user/{}/v_log".format(myscores['userId']), "w", encoding="utf8") as fp:
                    fp.write(str(v_log))
                print("检测到视频数量分数已满,退出学习")
                break

        try_count = 0
        while True:
            if myscores['视听学习时长'] < myscores['视听学习时长目标'] and try_count < 10:
                num_time = 60
                driver_video.get_url(links[v_log-1])
                time.sleep(random.randint(2, 5))
                remaining = (myscores['视听学习时长目标'] - myscores['视听学习时长']) * 3 * num_time
                print("剩下时长是：{}".format(remaining))
                lifetime += remaining
                for i in range(remaining):
                    if random.random() > 0.5:
                        driver_video.go_js(
                            'window.scrollTo(0, (document.body.scrollHeight-1000)/{}*{})'.format(remaining, i))
                    print("\r视频学习中，视频总时长剩余{}秒".format(remaining - i - 1), end="")
                    time.sleep(1)

                    '''
                    if i % (180) == 0 and i != remaining:
                        total, each, dtotal, deach, myscores = show_score(driver_video.get_cookies())
                        if myscores['视听学习时长'] >= timetarget:
                            print("检测到视频时长分数已满,退出学习")
                            break
                    '''
                print('')
                # driver_video.go_js('window.scrollTo(0, document.body.scrollHeight)')
                myscores.update(show_scorenew(driver_video))
            else:
                print("检测到视频时长分数已满,退出学习")
                break

        if try_count < 10:
            print("视频学习完成")
        else:
            print("视频学习出现异常，请检查用户名下v_log文件记录数")
        # driver_video.quit()
        print("视频学习共用时长：{}".format(lifetime))
    else:
        print("视频之前学完了")


if __name__ == '__main__':
    #  0 读取版本信息
    start_time = time.time()
    #info_shread = threads.MyThread("获取更新信息...", version.up_info)
    #info_shread.start()
    #  1 创建用户标记，区分多个用户历史纪录
    dd_status, uname = user.get_user()
    cookies = user_flag(dd_status, uname)
    myscores = show_score(cookies)
    print(myscores['inBlackList'])
    # 检查userId目录
    userId = myscores['userId']
    dd, userId = user.get_userId(userId)
    # 读取历史记录
    a_log, v_log = user.get_log(dd, userId)
    '''
    print('1',cookies)
    driver_article = mydriver.Mydriver(nohead = False)
    driver_article.get_url("https://www.xuexi.cn/notFound.html")
    print('2',driver_article.get_cookies())
    #driver_article.set_cookies(cookies)
    print('3',driver_article.get_cookies())
    '''
    driver_login = mydriver.Mydriver(noimg=True, nohead=True)
    driver_login.get_url('https://www.xuexi.cn/notFound.html')
    driver_login.set_cookies(cookies)
    print('开始今天的文章学习')
    article(driver_login, a_log, myscores)
    print('开始今天的视频学习')
    video(driver_login, v_log, myscores)
    print("总计用时{}分钟{}秒" .format(int(time.time() - start_time) // 60, int(time.time() - start_time) % 60))
    driver_login.quit()
    # user.shutdown(60)
'''
    nohead, lock, stime = get_argv()
    article_thread = threads.MyThread("文章学习", article, driver_login, a_log, each, lock=lock)
    video_thread = threads.MyThread("视频学习", video, driver_login, v_log, each, lock=lock)
    article_thread.start()
    video_thread.start()
    article_thread.join()
    video_thread.join()


    print("总计用时" + str(int(time.time() - start_time) / 60) + "分钟")
    user.shutdown(stime)
'''