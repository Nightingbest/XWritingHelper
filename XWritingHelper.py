import tkinter as tk
from screeninfo import get_monitors
import pyautogui
import time
import threading
import ctypes
import keyboard

class WritingHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("赛博打字机")
        
        # 获取屏幕分辨率
        monitors = get_monitors()
        screen_width = monitors[0].width
        screen_height = monitors[0].height
        
        # 创建窗口
        window_width = int(screen_width * 0.2)
        window_height = int(screen_height * 0.2)
        self.root.geometry(f"{window_width}x{window_height}+{int((screen_width-window_width)/2)}+{int((screen_height-window_height)/2)}")
        
        # 添加标签显示默认信息
        default_text = "点击【开始】，5秒后自动输入,esc中断输入"
        self.default_label = tk.Label(self.root, text=default_text, fg="gray", font=("Helvetica", 12))
        self.default_label.place(relx=0.5, rely=0.1, anchor="center")  # 调整y轴位置

        # 添加文本输入框
        self.text_entry = tk.Text(self.root, height=10, width=40)
        self.text_entry.pack(pady=10)
        self.text_entry.place(relx=0.5, rely=0.5, anchor="center")  # 调整y轴位置

        # 添加开始按钮
        self.start_stop_button = tk.Button(self.root, text="开始", command=self.start_stop_action, height=2, width=10)
        self.start_stop_button.place(relx=0.3, rely=0.8, anchor="center")  # 调整按钮位置

        # 添加退出按钮
        self.quit_button = tk.Button(self.root, text="退出", command=self.root.quit, height=2, width=10)
        self.quit_button.place(relx=0.7, rely=0.8, anchor="center")  # 调整按钮位置
        
        # 变量用于存储用户输入的内容
        self.user_input = None
        
        # 记录文本框是否可编辑的状态
        self.text_editable = True

        # 用于停止输入的标志
        self.stop_typing_flag = False

    def start_stop_action(self):
        current_text = self.start_stop_button.cget("text")
        if current_text == "开始":
            self.start_stop_button.config(text="停止")
            # 禁用文本框编辑
            self.text_entry.config(state=tk.DISABLED)
            # 隐藏默认信息标签
            self.default_label.pack_forget()
            # 存储用户输入的内容
            self.user_input = self.text_entry.get("1.0", tk.END).strip()
            # 更新文本框可编辑状态的记录
            self.text_editable = False
            
            # 启动模拟输入的线程
            self.start_typing_thread()
        else:
            self.stop_typing()

    def start_typing_thread(self):
        typing_thread = threading.Thread(target=self.simulate_typing_thread)
        typing_thread.start()

    def simulate_typing_thread(self):
        # 等待5秒
        time.sleep(5)
        # 获取用户输入的文本
        text = self.text_entry.get("1.0", tk.END).strip()
        # 监听esc键的按下事件,设置停止标志
        keyboard.on_press_key("esc", self.stop_typing)

        # 模拟键盘输入
        for char in text:
            if self.stop_typing_flag:
                break
            pyautogui.write(char)
        
        # 恢复相关界面状态
        self.restore_ui_state()

    def stop_typing(self, event):
        # 停止模拟输入
        self.stop_typing_flag = True

    def restore_ui_state(self):
        # 更新按钮为开始
        self.start_stop_button.config(text="开始")
        # 启用文本框编辑
        self.text_entry.config(state=tk.NORMAL)
        # 显示默认信息标签
        self.default_label.pack()
        # 清空存储的用户输入内容
        self.user_input = None
        # 更新文本框可编辑状态的记录
        self.text_editable = True
        # 重置停止输入的标志
        self.stop_typing_flag = False
        # 取消esc键的按下事件监听
        keyboard.unhook_key("esc")

SW_HIDE = 0
HWND = ctypes.windll.kernel32.GetConsoleWindow()
ctypes.windll.user32.ShowWindow(HWND, SW_HIDE)

if __name__ == "__main__":
    root = tk.Tk()
    app = WritingHelper(root)
    root.mainloop()