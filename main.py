import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os  

# 预留接口导入
try:
    from wave2D import wave_main
except ImportError:
    def wave_main():
        messagebox.showinfo("提示", "wave2D 模块未找到或未实现。")

try:
    from heat2D import heat_main
except ImportError:
    def heat_main():
        messagebox.showinfo("提示", "heat2D 模块未找到或未实现。")

try:
    from laplace2D import laplace_main
except ImportError:
    def laplace_main():
        messagebox.showinfo("提示", "laplace2D 模块未找到或未实现。")

try:
    from classification_demo import classification_main
except ImportError:
    def classification_main():
        messagebox.showinfo("提示", "classification_demo 模块未找到或未实现。")

# 主窗口初始化
root = tk.Tk()
root.title("偏微分方程可视化实验平台")
root.geometry("600x550")
root.configure(bg="#f0f4f8")

# 样式设置
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), padding=10)
style.configure('Header.TLabel', font=('Helvetica', 20, 'bold'), background="#f0f4f8")
style.configure('Sub.TLabel', font=('Helvetica', 12), background="#f0f4f8")

# 标题
header = ttk.Label(root, text="偏微分方程可视化实验平台", style='Header.TLabel')
header.pack(pady=20)

# 子标题
sub = ttk.Label(root, text="请选择一个模块进入模拟演示", style='Sub.TLabel')
sub.pack(pady=5)

# 按钮容器
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=30)

# 各模块按钮
buttons = [
    ("二维波动方程", wave_main),
    ("二维热传导方程", heat_main),
    ("二维调和方程", laplace_main),
    ("PDE分类与化简", classification_main)
]

for i, (text, command) in enumerate(buttons):
    btn = ttk.Button(button_frame, text=text, command=command, width=25)
    btn.grid(row=i, column=0, padx=10, pady=10)

# 退出按钮
def force_exit():
    root.destroy()
    os._exit(0)
    
exit_btn = ttk.Button(root, text="退出程序", command=force_exit, width=15)
exit_btn.pack(pady=10)

# 运行主循环
root.mainloop()
