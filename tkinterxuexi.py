from PIL import Image,ImageTk
import tkinter as tk

# 简单插入显示
def show_jpg():
    root = tk.Tk()

    # 二维码区
    L_QRCode = tk.LabelFrame(root, width=100, height=100, text='扫描下方二维码', padx=10, pady=10)
    L_QRCode.grid(row=0, column=0, rowspan=3)
    img = Image.open('./user/QRCode.png')  # 打开图片
    img = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    imglabel = tk.Label(L_QRCode, image=img)
    imglabel.grid(row=0, column=0)

    vs_label = tk.Label(root, text='娄阔峰')  # app_name + 'V' + str(app_version))
    vs_label.grid(row=3, column=0, sticky=tk.W)

    L = tk.LabelFrame(root, width=100, height=100, padx=5, pady=5, borderwidth=0)
    L.grid(row=0, column=1, rowspan=3, sticky=tk.N+tk.S)

    L_scores = tk.LabelFrame(L, width=460, height=120, text='学习情况')
    L_scores.grid(row=0, column=0, rowspan=1, columnspan=3, sticky=tk.E+tk.W)
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
    L_Message.grid(row=1, column=0, rowspan=3, columnspan=3, sticky=tk.E+tk.W)
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
    root.mainloop()

if __name__ == '__main__':
    show_jpg()
