import tkinter as tk
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageTk
from selenium.webdriver import ActionChains
import time
import random
import re  # 正则
import access  # 数据库
from config import *

#我添加的内容
from lxml import etree





class Work(tk.Tk):
    def __init__(self, *args, **kw):
        super().__init__()
        self.run()
        #self.refresh_data()
        self.mainloop()

    def run(self):
        self.wm_title('学习强国 实干兴邦')
        #self.wm_minsize(800, 600)  # 设置窗口最小化大小
        #self.wm_maxsize(800, 600)  # 设置窗口最大化大小
        self.resizable(width=False, height=False)

        # 积分情况
        L = tk.LabelFrame(self, width=100, height=100, padx=5, pady=5, borderwidth=0)
        L.grid(row=0, column=1, rowspan=3, sticky=tk.N + tk.S)

        L_scores = tk.LabelFrame(L, width=460, height=120, text='学习情况')
        L_scores.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=tk.E + tk.W)
        # 学习分数情况
        jf_label1 = tk.Label(L_scores, text='总积分：0')
        jf_label1.grid(row=0, column=0, columnspan=1)
        jf_label2 = tk.Label(L_scores, text='今日积分：0')
        jf_label2.grid(row=0, column=1, columnspan=1)

        jf_label3 = tk.Label(L_scores, text='文章篇数：0/0')
        jf_label3.grid(row=1, column=0, columnspan=1)
        jf_label4 = tk.Label(L_scores, text='文章时长：0/0')
        jf_label4.grid(row=1, column=1, columnspan=1)

        jf_label5 = tk.Label(L_scores, text='视频个数：0/0')
        jf_label5.grid(row=2, column=0, columnspan=1)
        jf_label6 = tk.Label(L_scores, text='视频时长：0/0')
        jf_label6.grid(row=2, column=1, columnspan=1)

        jf_label7 = tk.Label(L_scores, text='点点通：0')
        jf_label7.grid(row=3, column=0, columnspan=1)
        jf_label8 = tk.Label(L_scores, text='有效浏览：0/0')
        jf_label8.grid(row=3, column=1, columnspan=1)

        jf_label9 = tk.Label(L_scores, text='有效视听：0/0')
        jf_label9.grid(row=4, column=0, columnspan=1)
        jf_label10 = tk.Label(L_scores, text='挑战答题：0/0')
        jf_label10.grid(row=4, column=1, columnspan=1)

        # 程序信息框
        L_Message = tk.LabelFrame(L, width=10, height=30, text='登录信息', padx=10, pady=10)
        L_Message.grid(row=1, column=0, rowspan=3, columnspan=3, sticky=tk.E + tk.W)
        L_listbox = tk.Listbox(L_Message, width=25, height=15)
        L_listbox.grid(row=0, column=0)

        # 下一篇按钮
        next = tk.Button(L, text='下一篇', command=lambda: next_one())
        next.grid(row=5, column=0)

        # 清空历史按钮
        clean = tk.Button(L, text='清空历史', command=lambda: clean_history())
        clean.grid(row=5, column=1)

        # 退出按钮
        ext = tk.Button(L, text='退出', command=lambda: app_quit(self))
        ext.grid(row=5, column=2)

        R = tk.LabelFrame(self, width=100, height=100, padx=5, pady=5, borderwidth=0)
        R.grid(row=0, column=0, rowspan=3, sticky=tk.N + tk.S)
        # 二维码区
        L_QRCode = tk.LabelFrame(R, width=455, height=455, text='扫描下方二维码', padx=10, pady=10)
        L_QRCode.grid(row=0, column=0, rowspan=3)
        imglabel = tk.Label(L_QRCode, width=45, height=26)
        imglabel.grid(row=0, column=0)

        img = Image.open('./user/QRCode.png')  # 打开图片
        img = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
        imglabel.image = img

        # 版本号
        global server
        #server = checkApp()
        vs_label = tk.Label(R, text='娄阔峰')#app_name + 'V' + str(app_version))
        vs_label.grid(row=3, column=0, sticky=tk.W)

        # self.fill_pic(imglabel)

    def fill_pic(self, imglabel):
        img = Image.open('./user/QRCode.png')  # 打开图片
        img = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
        imglabel.image = img


    def show_log_right(self, g_msg):
        self.L.inser(g_msg)
        print('aaa')

    def seach_qr(self):
        url = 'https://pc.xuexi.cn/points/login.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'}
        r = requests.get(url, headers=headers)
        selector = etree.HTML(r.text)
        selector.xpath("//img[@src]")

    def refresh_data(self):  # 需要刷新数据的操作
        if getQr == False:
            g_msg = seach_qr()  # 查找二维码
            show_log_right(g_msg)

        if Login == False:
            fill_pic(self)
            show_log_right(waitToScan())  # 等待扫描
            self.after(2000, self.refresh_data)
        else:  # 登录成功
            # if video_is_open == False and artic_is_open == False:
            pic_label.destroy()  # 销毁二维码控件
            if getJifen == False:
                show_log_right(flash_coin())  # 获取积分
                self.after(2000, self.refresh_data)
            else:
                if (coin_a_today < coin_a_total) or (coin_a_l_today < coin_a_l_total):  # 如果文章篇数没学满,或时长不足
                    if artic_is_open == False:
                        if news == []:
                            show_log_right('文章板块：%s' % a_chapter[chapter_index]['title'])
                            show_log_right(get_news_list(a_chapter[chapter_index]))
                            self.after(2000, self.refresh_data)  # 毫秒
                        else:
                            listname_label = tk.Label(self,
                                                      text='文章板块：' + a_chapter[chapter_index]['title'] + '（共 ' + str(
                                                          len(news)) + ' 篇）')
                            listname_label.place(x=20, y=20, anchor='nw')
                            # 创建学习列表控件
                            l_left = tk.Listbox(self, width=47, height=17)
                            l_left.place(x=20, y=45, anchor='nw')
                            for i in range(1, len(news) + 1):
                                l_left.insert(0, '文章' + str(i) + '：' + news[i - 1].get_attribute('innerHTML'))
                            if read_index < len(news):
                                if check_record_exist(news[read_index].get_attribute('innerHTML')):  # 检测数据库是否有
                                    show_log_right('跳过已学：' + news[read_index].get_attribute('innerHTML'))
                                    read_index = read_index + 1
                                else:
                                    show_log_right(openArticle(news[read_index]))
                                    starTime = int(time.time())
                            else:
                                turnPage = True  # 构造跳转下一页的条件
                                artic_is_open = True  # 构造跳转下一页的条件
                            self.after(2000, self.refresh_data)  # 单位为毫秒
                    else:  # 滚动文章
                        nowTime = int(time.time())
                        if (starTime + random.randint(325, 350)) > nowTime and turnPage == False:  # 学习时间 每篇至少320秒才不浪费
                            show_log_right(roll_page(random.randint(50, 2000)))
                            self.after(10000, self.refresh_data)  # 单位为毫秒
                        else:  # 下一篇文章
                            print(u'下一篇文章')
                            turnPage = False
                            show_log_right(flash_coin())  # 刷新积分
                            read_index = read_index + 1
                            starTime = int(time.time())
                            if read_index < len(news):
                                show_log_right(openArticle(news[read_index]))
                            else:
                                driver.switch_to.window(list_win_handle)
                                cur_window = list_win_handle
                                if coin_a_today < coin_a_total or coin_a_l_today < coin_a_l_total:  # 如果文章积分全部获取就会自动学视频
                                    if has_next_page:  # 如果有下一页
                                        show_log_right('切换下一页继续学习...')
                                        news = get_next_page_list(a_chapter[chapter_index])
                                        read_index = 0
                                        artic_is_open = False
                                    else:
                                        show_log_right('(╰_╯)本次文章学习未满分')
                                        show_log_right('切换板块后继续学习...')
                                        read_index = 0
                                        chapter_index = chapter_index + 1
                                        if chapter_index >= len(a_chapter):
                                            chapter_index = 0
                                        news = []  # 置空以便重新获取
                                        artic_is_open = False
                                else:
                                    read_index = 0
                            self.after(1000, self.refresh_data)  # 单位为毫秒
                elif (coin_v_today < coin_v_total) or (coin_v_l_today < coin_v_l_total):  # 如果视频个数没学满
                    if video_is_open == False:
                        if videos == []:
                            show_log_right('视频板块：%s' % v_chapter[chapter_index]['title'])
                            show_log_right(get_video_list(v_chapter[chapter_index]))
                            self.after(2000, self.refresh_data)  # 毫秒
                        else:
                            listname_label = tk.Label(self,
                                                      text='视频板块：' + v_chapter[chapter_index]['title'] + '（共 ' + str(
                                                          len(videos)) + ' 个）')
                            listname_label.place(x=20, y=20, anchor='nw')
                            # 创建学习列表控件
                            l_left = tk.Listbox(self, width=47, height=17)
                            l_left.place(x=20, y=45, anchor='nw')
                            if read_index < len(videos):
                                for i in range(1, len(videos) + 1):
                                    l_left.insert(0, '视频' + str(i) + '：' + videos[i - 1].get_attribute('innerHTML'))
                                if check_record_exist(videos[read_index].get_attribute('innerHTML')):  # 检测数据库是否有
                                    show_log_right('跳过已学：' + videos[read_index].get_attribute('innerHTML'))
                                    read_index = read_index + 1
                                else:
                                    show_log_right(openVideo(videos[read_index]))
                                    starTime = int(time.time())
                            else:
                                turnPage = True  # 构造跳转下一页的条件
                                video_is_open = True  # 构造跳转下一页的条件
                            self.after(2000, self.refresh_data)  # 单位为毫秒
                    else:  # 滚动视频界面
                        nowTime = int(time.time())
                        if video_is_over == False and turnPage == False:
                            show_log_right(roll_page(random.randint(50, 100)))
                            rstr = check_video_over()
                            if rstr == True:
                                video_is_over = True
                                show_log_right('视频播放结束，准备切换下一个...')
                            else:
                                show_log_right(rstr)
                            self.after(10000, self.refresh_data)  # 单位为毫秒
                        else:  # 下一个
                            print(u'下一个视频')
                            video_is_over = False
                            turnPage = False
                            show_log_right(flash_coin())  # 刷新积分
                            read_index = read_index + 1
                            if read_index < len(videos):
                                starTime = int(time.time())
                                show_log_right(openVideo(videos[read_index]))
                            else:
                                driver.switch_to.window(list_win_handle)
                                cur_window = list_win_handle
                                if coin_v_today < coin_v_total or coin_v_l_today < coin_v_l_total:  # 如果视频积分也全部获取则结束
                                    if has_next_page:  # 如果有下一页
                                        show_log_right('切换下一页继续学习...')
                                        videos = get_next_page_list(v_chapter[chapter_index])
                                        read_index = 0
                                        video_is_open = False
                                    else:
                                        show_log_right('(╰_╯)本次视频学习未满分')
                                        show_log_right('切换板块后继续学习...')
                                        read_index = 0
                                        chapter_index = chapter_index + 1
                                        if chapter_index >= len(v_chapter):
                                            chapter_index = 0
                                        videos = []  # 置空以便重新获取
                                        video_is_open = False
                                else:
                                    read_index = 0
                            self.after(1000, self.refresh_data)  # 单位为毫秒
                else:
                    driver.quit()

if __name__ == '__main__':
    Work(tk.Tk)
