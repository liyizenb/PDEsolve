import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rcParams
from tkinter import Toplevel, Label, Button, StringVar, Radiobutton, Entry, messagebox

# 中文支持
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

def heat_main():
    # 弹窗选择初始热量场类型
    init_choice = StringVar(value="default")

    def run_simulation():
        mode = init_choice.get()
        expr = expr_entry.get() if mode == "custom" else None
        try:
            interval_ms = int(speed_entry.get())
        except ValueError:
            messagebox.showerror("输入错误", "动画速度必须是整数！")
            return
        input_win.destroy()
        start_simulation(expr, interval_ms)

    input_win = Toplevel()
    input_win.title("选择初始热量分布")
    Label(input_win, text="请选择初始热量分布方式：").pack(pady=5)
    Radiobutton(input_win, text="默认中心加热", variable=init_choice, value="default").pack()
    Radiobutton(input_win, text="自定义表达式", variable=init_choice, value="custom").pack()

    Label(input_win, text="输入表达式（变量为 x, y, 使用 np 函数）:").pack()
    expr_entry = Entry(input_win, width=50)
    expr_entry.insert(0, "np.exp(-100*((x-0.5)**2 + (y-0.5)**2))")
    expr_entry.pack(pady=5)

    Label(input_win, text="输入动画速度（毫秒/帧，默认20）:").pack()
    speed_entry = Entry(input_win, width=10)
    speed_entry.insert(0, "20")
    speed_entry.pack(pady=5)

    Button(input_win, text="开始模拟", command=run_simulation).pack(pady=10)

def start_simulation(expr_str=None, interval=20):
    # 参数设置
    alpha = 0.01
    Lx, Ly = 1.0, 1.0
    Nx, Ny = 100, 100
    dx = Lx / Nx
    dy = Ly / Ny
    dt = 0.001
    T = 2.0
    steps = int(T / dt)

    cfl = alpha * dt * (1 / dx**2 + 1 / dy**2)
    if cfl >= 0.5:
        raise ValueError(f"CFL 条件不满足，当前CFL={cfl:.3f}，应 < 0.5")

    # 网格
    x = np.linspace(0, Lx, Nx)
    y = np.linspace(0, Ly, Ny)
    X, Y = np.meshgrid(x, y, indexing='ij')

    # 初始条件
    u = np.zeros((Nx, Ny))
    if expr_str:
        try:
            u = eval(expr_str, {"np": np, "x": X, "y": Y})
        except Exception as e:
            messagebox.showerror("表达式错误", f"自定义初始表达式出错：\n{e}")
            return
    else:
        u[(X - 0.5)**2 + (Y - 0.5)**2 < 0.01] = 1.0

    def step_heat(u):
        u_new = np.copy(u)
        u_new[1:-1, 1:-1] = u[1:-1, 1:-1] + alpha * dt * (
            (u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1]) / dx**2 +
            (u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2]) / dy**2
        )
        return u_new

    # 可视化
    fig, ax = plt.subplots()
    img = ax.imshow(u, extent=[0, Lx, 0, Ly], cmap='hot', vmin=0, vmax=1, animated=True)
    ax.set_title("二维热传导方程演化")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # 动画更新函数
    def update(frame):
        nonlocal u
        u = step_heat(u)
        img.set_array(u)
        return [img]

    ani = animation.FuncAnimation(fig, update, frames=300, interval=interval, blit=True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    heat_main()
