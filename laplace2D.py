import numpy as np
import matplotlib.pyplot as plt
from tkinter import Toplevel, Label, Button, StringVar, Radiobutton, Entry, messagebox
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False


def laplace_main():
    # === 弹窗输入界面 ===
    mode = StringVar(value="default")

    def run_sim():
        selected_mode = mode.get()
        if selected_mode == "default":
            input_win.destroy()
            solve_laplace()
        else:
            try:
                bc = {
                    'left': eval(left_entry.get(), {"np": np, "x": y}),
                    'right': eval(right_entry.get(), {"np": np, "x": y}),
                    'top': eval(top_entry.get(), {"np": np, "x": x}),
                    'bottom': eval(bottom_entry.get(), {"np": np, "x": x}),
                }
                expr = center_entry.get()
                input_win.destroy()
                solve_laplace(boundary_conditions=bc, center_expr=expr)
            except Exception as e:
                messagebox.showerror("错误", f"边界或初值表达式错误：\n{e}")
                return

    # 网格预先准备供表达式使用
    Nx, Ny = 100, 100
    Lx, Ly = 1.0, 1.0
    x = np.linspace(0, Lx, Nx)
    y = np.linspace(0, Ly, Ny)

    input_win = Toplevel()
    input_win.title("边界条件设置")
    Label(input_win, text="选择边界条件方式：").pack(pady=5)
    Radiobutton(input_win, text="默认左边界为1，其余为0", variable=mode, value="default").pack(anchor='w')
    Radiobutton(input_win, text="自定义边界条件", variable=mode, value="custom").pack(anchor='w')

    Label(input_win, text="左边界 u(0,y):").pack()
    left_entry = Entry(input_win, width=40)
    left_entry.insert(0, "1.0")
    left_entry.pack()

    Label(input_win, text="右边界 u(Lx,y):").pack()
    right_entry = Entry(input_win, width=40)
    right_entry.insert(0, "0.0")
    right_entry.pack()

    Label(input_win, text="上边界 u(x,Ly):").pack()
    top_entry = Entry(input_win, width=40)
    top_entry.insert(0, "0.0")
    top_entry.pack()

    Label(input_win, text="下边界 u(x,0):").pack()
    bottom_entry = Entry(input_win, width=40)
    bottom_entry.insert(0, "0.0")
    bottom_entry.pack()

    Label(input_win, text="中间区域初始值表达式（可选，变量 x,y）:").pack()
    center_entry = Entry(input_win, width=50)
    center_entry.insert(0, "0.0")
    center_entry.pack()

    Button(input_win, text="开始模拟", command=run_sim).pack(pady=10)

    # === Laplace 解算函数 ===
    def solve_laplace(boundary_conditions=None, center_expr=None):
        dx = Lx / (Nx - 1)
        dy = Ly / (Ny - 1)
        tol = 1e-5
        max_iter = 10000
        uniform_tol = 1e-4

        u = np.zeros((Nx, Ny))
        u_new = np.zeros_like(u)

        X, Y = np.meshgrid(x, y, indexing='ij')

        # 初始中心区域
        if center_expr:
            try:
                u = eval(center_expr, {"np": np, "x": X, "y": Y})
            except Exception as e:
                messagebox.showerror("表达式错误", f"中心初值表达式错误：\n{e}")
                return

        if boundary_conditions:
            u[0, :] = boundary_conditions['left']
            u[-1, :] = boundary_conditions['right']
            u[:, -1] = boundary_conditions['top']
            u[:, 0] = boundary_conditions['bottom']
        else:
            u[0, :] = 1.0

        # 迭代计算
        converged = False
        reason = ""
        for it in range(max_iter):
            u_new[1:-1, 1:-1] = 0.25 * (
                u[2:, 1:-1] + u[:-2, 1:-1] +
                u[1:-1, 2:] + u[1:-1, :-2]
            )

            # 重设边界
            if boundary_conditions:
                u_new[0, :] = boundary_conditions['left']
                u_new[-1, :] = boundary_conditions['right']
                u_new[:, -1] = boundary_conditions['top']
                u_new[:, 0] = boundary_conditions['bottom']
            else:
                u_new[0, :] = 1.0
                u_new[-1, :] = 0
                u_new[:, 0] = 0
                u_new[:, -1] = 0

            if not np.all(np.isfinite(u_new)):
                reason = f"第 {it} 次迭代出现 NaN/Inf，强制终止。"
                break

            error = np.max(np.abs(u_new - u))
            maxdiff = np.max(u_new) - np.min(u_new)
            u[:, :] = u_new

            if error < tol:
                converged = True
                reason = f"收敛于第 {it} 次迭代，误差为 {error:.2e}"
                break
            if maxdiff < uniform_tol:
                converged = True
                reason = f"温度场趋于均匀，第 {it} 次迭代提前终止（最大差值 {maxdiff:.2e}）"
                break
        else:
            reason = "未能在最大迭代次数内收敛"

        # 弹窗提示收敛结果
        messagebox.showinfo("计算完成", reason)

        # 可视化
        fig, ax = plt.subplots()
        im = ax.imshow(u, extent=[0, Lx, 0, Ly], cmap='hot', origin='lower')
        ax.set_title("Laplace 方程稳态解")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        fig.colorbar(im, ax=ax, label="温度")
        plt.tight_layout()
        plt.show()
