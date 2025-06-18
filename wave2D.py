import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Toplevel, Label, Entry, Button, Radiobutton, StringVar, messagebox
from matplotlib import rcParams
from mpl_toolkits.mplot3d import Axes3D

# 中文显示设置（适用于 Windows）
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

def wave_main():
    # 创建自定义初始条件窗口
    def run_simulation():
        try:
            u_expr = u_entry.get()
            ut_expr = ut_entry.get()
            speed = int(speed_entry.get())
        except Exception as e:
            messagebox.showerror("输入错误", f"请输入有效的速度或表达式。\n{e}")
            return
        input_win.destroy()
        start_simulation(u_expr, ut_expr, speed)

    input_win = Toplevel()
    input_win.title("自定义初始条件")
    Label(input_win, text="初始位移表达式 u(x,y)：").pack()
    u_entry = Entry(input_win, width=50)
    u_entry.insert(0, "np.exp(-200*((x-0.5)**2 + (y-0.5)**2))")
    u_entry.pack(pady=5)
    Label(input_win, text="初始速度表达式 u_t(x,y)：").pack()
    ut_entry = Entry(input_win, width=50)
    ut_entry.insert(0, "0")
    ut_entry.pack(pady=5)
    Label(input_win, text="动画播放速度 (毫秒/帧)：").pack()
    speed_entry = Entry(input_win, width=10)
    speed_entry.insert(0, "20")
    speed_entry.pack(pady=5)
    Button(input_win, text="开始模拟", command=run_simulation).pack(pady=10)

    def start_simulation(u_expr, ut_expr, speed):
        # 参数设置
        c = 1.0
        Lx, Ly = 1.0, 1.0
        Nx, Ny = 100, 100
        dx = Lx / Nx
        dy = Ly / Ny
        dt = 0.001
        X, Y = np.meshgrid(np.linspace(0, Lx, Nx), np.linspace(0, Ly, Ny), indexing='ij')

        cfl = c * dt * np.sqrt(1 / dx**2 + 1 / dy**2)
        if cfl >= 1:
            raise ValueError(f"CFL 条件不满足，当前 CFL={cfl:.2f}，应 < 1")

        # 初始条件
        try:
            u = eval(u_expr, {"np": np, "x": X, "y": Y})
            ut = eval(ut_expr, {"np": np, "x": X, "y": Y})
        except Exception as e:
            messagebox.showerror("表达式错误", f"初始条件表达式有误：\n{e}")
            return

        u_old = u - dt * ut  # 从速度构造出前一时刻

        # 更新函数
        def step_wave(u, u_old):
            u_new = np.zeros_like(u)
            u_new[1:-1, 1:-1] = (2 * u[1:-1, 1:-1] - u_old[1:-1, 1:-1] +
                (c**2 * dt**2) * (
                    (u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1]) / dx**2 +
                    (u[1:-1, 2:] - 2*u[1:-1, 1:-1] + u[1:-1, :-2]) / dy**2))
            return u_new

        # 三维可视化
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_zlim(-1, 1)
        ax.set_title("二维波动方程三维演化")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("u(x, y, t)")

        surf = [ax.plot_surface(X, Y, u, cmap='viridis')]

        def update(frame):
            nonlocal u, u_old, surf
            u_new = step_wave(u, u_old)
            u_old, u = u, u_new
            # 清除旧图面
            for coll in surf:
                coll.remove()
            surf = [ax.plot_surface(X, Y, u, cmap='viridis')]
            return surf

        ani = animation.FuncAnimation(fig, update, frames=300, interval=speed, blit=False)
        plt.tight_layout()
        plt.show()

