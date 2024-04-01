import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import videoprocess as vp
import trainingsetprocess as tp
import videocapture as vc

def center_window(root, width=400, height=200):
    """窗口居中显示"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def update_flag_options(*args):
    """根据选择的menu更新flag的选项"""
    menu_choice = menu_mapping[menu_var.get()]
    if menu_choice in (1, 2):  # 当用户选择了检测模式后，才允许选择flag
        flag_combobox.config(state="readonly")
    else:
        flag_combobox.config(state="disabled")

def detect_action():
    menu = menu_mapping[menu_var.get()]
    flag = flag_mapping[flag_var.get()]
    if menu == 1:  # 从本地导入视频检测
        video_path = filedialog.askopenfilename()  # 弹出文件选择框
        if video_path:  # 确保用户选择了文件
            tp.process_training_set(flag)
            vp.process_video_input(flag,video_path)
    elif menu == 2:  # 调用摄像头检测
        tp.process_training_set(flag)
        vc.process(flag)

# 映射文字信息到数字
menu_mapping = {"从本地导入视频检测": 1, "调用摄像头检测": 2}
flag_mapping = {"俯卧撑": 1, "深蹲": 2, "引体向上": 3}

# 创建主窗口
root = tk.Tk()
root.title("运动检测系统")

# 窗口居中
center_window(root, 400, 200)

# 创建变量
menu_var = tk.StringVar()
flag_var = tk.StringVar()

# 创建检测模式下拉列表
menu_label = ttk.Label(root, text="选择检测模式：")
menu_label.pack(pady=5)
menu_combobox = ttk.Combobox(root, textvariable=menu_var, state="readonly")
menu_combobox['values'] = list(menu_mapping.keys())  # 使用文字信息
menu_combobox.bind('<<ComboboxSelected>>', update_flag_options)
menu_combobox.pack(pady=5)

# 创建运动类型下拉列表
flag_label = ttk.Label(root, text="选择运动类型：")
flag_label.pack(pady=5)
flag_combobox = ttk.Combobox(root, textvariable=flag_var, state="disabled")  # 初始状态禁用
flag_combobox['values'] = list(flag_mapping.keys())  # 使用文字信息
flag_combobox.pack(pady=5)

# 创建检测按钮
detect_button = ttk.Button(root, text="开始检测", command=detect_action)
detect_button.pack(pady=20)

# 运行主循环
root.mainloop()
