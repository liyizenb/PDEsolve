import tkinter as tk
import math
from tkinter import messagebox,scrolledtext
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


def classification_main():
    win = tk.Toplevel()
    win.title("二维二阶PDE分类与化简")
    win.geometry("450x350")

    tk.Label(win, text="请输入 PDE 系数 (A u_xx + 2B u_xy + C u_yy + D u_x + E u_y + F u + G = 0)").pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(pady=5)

    labels = ['A (u_xx):', 'B (u_xy，混合项系数一半):', 'C (u_yy):', 'D (u_x):', 'E (u_y):', 'F (u):', 'G (常数项):']
    entries = []

    for i, text in enumerate(labels):
        tk.Label(frame, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=3)
        e = tk.Entry(frame, width=12)
        e.grid(row=i, column=1)
        entries.append(e)

    def classify_pde(A, B, C):
        delta = B ** 2 - A * C
        if delta < 0:
            return "椭圆型 (Elliptic)"
        elif delta == 0:
            return "抛物型 (Parabolic)"
        else:
            return "双曲型 (Hyperbolic)"

    def pde_simplify(A, B, C, D, E, F, G):
        if A == C and B == 0:
            theta = 0.0
        else:
            if A == C:
                theta = math.pi / 4
                if B < 0:
                    theta = -theta
            else:
                tan_2theta = 2 * B / (A - C)
                theta = 0.5 * math.atan(tan_2theta)

        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        lambda1 = A * cos_t**2 + 2 * B * cos_t * sin_t + C * sin_t**2
        lambda2 = A * sin_t**2 - 2 * B * cos_t * sin_t + C * cos_t**2

        D_prime = D * cos_t + E * sin_t
        E_prime = -D * sin_t + E * cos_t

        return theta, lambda1, lambda2, D_prime, E_prime, F, G

    def show_pde(theta, lambda1, lambda2, D_prime, E_prime, F, G):
        u = sp.Function('u')
        xi, eta = sp.symbols('xi eta')

        eq = sp.Eq(
            lambda1 * u(xi, eta).diff(xi, 2)
            + lambda2 * u(xi, eta).diff(eta, 2)
            + D_prime * u(xi, eta).diff(xi)
            + E_prime * u(xi, eta).diff(eta)
            + F * u(xi, eta)
            + G,
            0
        )

        str=r'''
    $\begin{cases}
        \xi =x\cos \theta +y\sin \theta\\
        \eta =-x\sin \theta +y\cos \theta\\
    \end{cases}$
        '''+'\n其中:'
        str += r'$\theta='+sp.latex(theta)+'$\n\n$$'+sp.latex(eq)+'$$'
        root = tk.Tk()
        root.title("PDE 展示窗口")

        # 可滚动文本框
        text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Consolas", 12))
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 插入文本并设置为只读
        text_area.insert(tk.END, str)
        text_area.configure(state='normal')  # 可复制，但不能编辑

        # 启动窗口主循环
        root.mainloop()
        
    def on_confirm():
        try:
            vals = [float(e.get()) for e in entries]
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效数字！")
            return

        A, B, C, D, E, F, G = vals
        pde_type = classify_pde(A, B, C)
        messagebox.showinfo("PDE类型判定", f"判别式 B^2 - A*C = {B ** 2 - A * C:.4f}\n该 PDE 类型为：{pde_type}")

        theta, lambda1, lambda2, D_prime, E_prime, F, G = pde_simplify(A, B, C, D, E, F, G)
        show_pde(theta, lambda1, lambda2, D_prime, E_prime, F, G)
        win.destroy()
        return 



    btn_confirm = tk.Button(win, text="确定", command=on_confirm)
    btn_confirm.pack(pady=15)
