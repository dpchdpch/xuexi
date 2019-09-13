import tkinter as tk
import tkinter.messagebox

root = tk.Tk()
root.title('Widgets')

width = 960
height = 800
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
root.geometry(size) # width*height + pos_x + pos_y

# label
# 最上方的那个黄条，后面的插件如果有事件都会修改这个黄条的值
myStr = tk.StringVar()
myStr.set('Label Default')
isHit = False

label = tk.Label(root,
    textvariable = myStr,
    bg = 'yellow', # =background
    font = ('Microsoft YaHei', 20),
    width = 60,  # 本例这里两个值单位是字节，不是像素
    height = 1
    )

label.grid(row=0, column=0,columnspan=6)

# button
# 每种插件都会包含在一个LabelFrame里
lf_button = tk.LabelFrame(root, width=96, height=96, text='Button')
lf_button.grid(row=1, column=0, sticky='w',padx=10)

def button_click():
    global isHit
    if isHit == False:
        isHit = True
        myStr.set('Label #1')
    else:
        isHit = False
        myStr.set('Label #2')

button = tk.Button(lf_button,
    text='Mod',
    width=10,
    height=3,
    command=button_click
    )
button.place(x=6,y=1)

# Scale
lf_Scale = tk.LabelFrame(root, width=460, height=120, text='Scale - HORIZONTAL')
lf_Scale.grid(row=2, column=0, sticky='w',padx=10,  columnspan=4)

def scale_click(v):
    myStr.set('You have selected '+ v)

scale = tk.Scale(lf_Scale,
    label='Scroll Me',
    from_ = 0,
    to = 100,
    orient = tk.HORIZONTAL,
    length = 440,
    showvalue = 1,
    tickinterval = 10,
    resolution = 1,
    command = scale_click
    )
scale.place(x=1,y=1)

# entry and text
lf_entry_text = tk.LabelFrame(root, width=160, height=240, text='Entry and Text')
lf_entry_text.grid(row=1, column=4, rowspan=2, padx = 6,  sticky='w')

entry = tk.Entry(lf_entry_text, relief='solid')
entry.place(x=6, y=1)

def button2_click():
    var = entry.get()
    textbox.insert('insert',var)


def button3_click():
    var = entry.get()
    textbox.insert('end',var)

button2 = tk.Button(lf_entry_text,
    text='inset curr',
    command=button2_click
    )
button2.place(x=6,y=32)

button3 = tk.Button(lf_entry_text,
    text='inset end',
    command=button3_click
    )
button3.place(x=80,y=32)

textbox = tk.Text(lf_entry_text,
    width=20,
    height=10,
    relief='solid'
    )
textbox.place(x=6,y=72)

# Listbox
lf_Listbox = tk.LabelFrame(root, width=260, height=240, text='Listbox')
lf_Listbox.grid(row=1, column=5, rowspan=2,  sticky='w')

myList = tk.StringVar()
myList.set(['default0','default1','default2'])
listbox = tk.Listbox(lf_Listbox,
    listvariable=myList,
    height=11
    )

# 为Listbox关联scrollbar
scrollbar = tk.Scrollbar(lf_Listbox,width=30, orient="vertical",command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.place(x=120, y=1, height=201)

for item in range(100):
    listbox.insert(0,item)

listbox.delete(0)

def button4_click():
    val = listbox.get(listbox.curselection())
    myStr.set(val)

button4 = tk.Button(lf_Listbox,
    text='display',
    width=10,
    height=2,
    command=button4_click
    )

listbox.place(x=6, y=1)
button4.place(x=164, y=1)


# Radio Button
lf_Radio = tk.LabelFrame(root, width=96, height=96, text='Radio')
lf_Radio.grid(row=1, column=2, sticky='w')

varRadio = tk.StringVar()
def radiobutton_click():
    myStr.set('You have selected ' + varRadio.get())

radio1 = tk.Radiobutton(lf_Radio,
    text='A',
    value='A',
    variable = varRadio,
    command=radiobutton_click
)

radio2 = tk.Radiobutton(lf_Radio,
    text='B',
    value='B',
    variable = varRadio,
    command=radiobutton_click
)



radio1.place(x=6, y=0)
radio2.place(x=6, y=30)


# Check Button
lf_Check = tk.LabelFrame(root, width=96, height=96, text='Check')
lf_Check.grid(row=1, column=1, sticky='w')

varCheck1 = tk.IntVar()
varCheck2 = tk.IntVar()

def checkbutton_click():
    if (varCheck1.get() == 1) & (varCheck2.get() == 1):
        myStr.set("Apple and Banana")
    elif (varCheck1.get() == 1) & (varCheck2.get() == 0):
        myStr.set("Apple")
    elif (varCheck1.get() == 0) & (varCheck2.get() == 1):
        myStr.set("Banana")
    else:
        myStr.set("Nothing")

checkbutton1 = tk.Checkbutton(lf_Check,
    text = 'Apple',
    variable = varCheck1,
    onvalue = 1,
    offvalue = 0,
    command = checkbutton_click
    )

checkbutton2 = tk.Checkbutton(lf_Check,
    text = 'Banana',
    variable = varCheck2,
    onvalue = 1,
    offvalue = 0,
    command = checkbutton_click
    )

checkbutton1.place(x=6, y=0)
checkbutton2.place(x=6, y=30)

# Menubar
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)

def dojob():
    pass

filemenu.add_command(label='New', command=dojob)
filemenu.add_command(label='Open', command=dojob)
filemenu.add_command(label='Save', command=dojob)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Cut', command=dojob)
editmenu.add_command(label='Copy', command=dojob)
editmenu.add_command(label='Paste', command=dojob)

submenu = tk.Menu(editmenu)
editmenu.add_cascade(label='Submenu', menu=submenu, underline=0)
submenu.add_command(label="Submenu1", command=dojob)
root.config(menu=menubar)

# Message Box
lf_MessageBox = tk.LabelFrame(root, width=96, height=96, text='MessageBox')
lf_MessageBox.grid(row=1, column=3, sticky='w')
def show_msg():
    tk.messagebox.showinfo(title='HI', message='Yahaha')

button4 = tk.Button(lf_MessageBox,
    text='Bing',
    width=10,
    height=3,
    command=show_msg
    )
button4.place(x=6,y=2)

# Menu Button
lf_MenuButton = tk.LabelFrame(root, width=96, height=96, text='MenuButton')
lf_MenuButton.grid(row=3, column=0, padx=10,sticky='w')

def menubutton_click1():
    myStr.set('You selected Apple.')

def menubutton_click2():
    myStr.set('You selected Banana.')

def menubutton_click3():
    myStr.set('You selected Coconut.')

menubutton = tk.Menubutton(lf_MenuButton,
    text="Fruits",
    relief='raised'
    )

menubutton.grid()
menubutton.menu = tk.Menu(menubutton,  tearoff=0)
menubutton["menu"] = menubutton.menu
menubutton.menu.add_command(label='Apple', command=menubutton_click1)
menubutton.menu.add_command(label='Banana', command=menubutton_click2)
menubutton.menu.add_command(label='Coconut', command=menubutton_click3)

menubutton.place(x=6,y=2)

# Option Menu
lf_OptionMenu = tk.LabelFrame(root, width=96, height=96, text='OptionMenu')
lf_OptionMenu.grid(row=3, column=1, sticky='w')

Options = ['Apple', 'Banana', 'Coconut']
op_var = tk.StringVar()
op_var.set(Options[0])
optionmenu = tk.OptionMenu(lf_OptionMenu,
    op_var,
    *Options
    )

def change_dropdown(*args):
    myStr.set("You have selected " + op_var.get())

op_var.trace('w', change_dropdown)

optionmenu.place(x=6,y=2)

# Spin Box
lf_SpinBox = tk.LabelFrame(root, width=96, height=96, text='SpinBox')
lf_SpinBox.grid(row=3, column=2, sticky='w')

spinbox = tk.Spinbox(lf_SpinBox,
    from_=0,
    to=10,
    width=8
    )
spinbox.place(x=6,y=2)

# Paned Window
lf_PanedWindow = tk.LabelFrame(root, width=570, height=96, text='PanedWindow')
lf_PanedWindow.grid(row=3, column=3, columnspan=3, sticky='w')

panedwindow = tk.PanedWindow(lf_PanedWindow, width=560)

pw_left = tk.Label(panedwindow, text="left pane")
panedwindow.add(pw_left)
pw_mid = tk.Label(panedwindow, text="mid pane")
panedwindow.add(pw_mid)
pw_right = tk.Label(panedwindow, text="right pane")
panedwindow.add(pw_right)

panedwindow.place(x=6,y=2)

# Canvas
lf_Canvas = tk.LabelFrame(root, width=935, height=410, text='Canvas')
lf_Canvas.grid(row=4, column=0, columnspan=6, padx=10, sticky='w')

canvas = tk.Canvas(lf_Canvas,
    bg = 'grey',
    heigh = 380,
    width = 900
    )
x0, y0, x1, y1 = 0,30,0,300
line = canvas.create_line(x0, y0, x1, y1)
oval = canvas.create_oval(x0+50, y0+50, x1+150, y1+50, fill='black')
arc  = canvas.create_arc(x0+160, y0, x1+310, y1, start = 30, extent = 150, fill = 'black')
rect = canvas.create_rectangle(560, 30, 870, 250)
poly = canvas.create_polygon(560, 220, 220, 310, 230, 190)
canvas.place(x=6,y=2)

root.mainloop()