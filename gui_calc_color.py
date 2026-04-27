import tkinter as tk
from tkinter import ttk, messagebox

# 可选倍率
OPTIONS = [2, 1.6, 1.3, 1.1]


def get_color_by_value(value):
    """
    根据数值大小返回颜色：
    5位数（10000~99999） -> 绿色
    十万级（100000~999999） -> 蓝色
    百万级（1000000~9999999） -> 黄色
    千万级及以上（10000000+） -> 红色
    其余 -> 黑色
    """
    try:
        n = abs(float(value))
    except:
        return "black"

    if n >= 10_000_000:
        return "red"
    elif n >= 1_000_000:
        return "#d4ac0d"   # 金黄色，比纯 yellow 更清楚
    elif n >= 100_000:
        return "blue"
    elif n >= 10_000:
        return "green"
    else:
        return "black"


def update_input_preview(*args):
    """
    当输入框内容变化时：
    1. 实时更新“当前输入”的显示
    2. 按数值级别改变输入文字颜色
    """
    text = number_var.get().strip()

    if text == "":
        current_input_var.set("未输入")
        entry_number.config(fg="black")
        input_value_label.config(fg="black")
        return

    try:
        value = float(text)
        color = get_color_by_value(value)

        # 输入框文字颜色
        entry_number.config(fg=color)

        # 当前输入显示
        if value.is_integer():
            display_text = f"{int(value)}"
        else:
            display_text = f"{value:g}"

        current_input_var.set(display_text)
        input_value_label.config(fg=color)

    except ValueError:
        current_input_var.set("输入无效")
        entry_number.config(fg="red")
        input_value_label.config(fg="red")


def calculate():
    """
    计算：输入数字 ÷ 选择倍率
    并根据结果数值级别改变结果颜色
    """
    try:
        number = float(number_var.get().strip())
        multiplier = float(combo_multiplier.get())
        result = number / multiplier

        # 处理显示格式
        if number.is_integer():
            number_text = str(int(number))
        else:
            number_text = f"{number:g}"

        if result.is_integer():
            result_text = str(int(result))
        else:
            result_text = f"{result:g}"

        # 当前输入也同步展示
        input_color = get_color_by_value(number)
        current_input_var.set(number_text)
        input_value_label.config(fg=input_color)
        entry_number.config(fg=input_color)

        # 结果展示
        result_color = get_color_by_value(result)
        result_value_var.set(result_text)
        result_value_label.config(fg=result_color)

        # 公式说明
        formula_var.set(f"{number_text} ÷ {multiplier} = {result_text}")

    except ValueError:
        messagebox.showerror("输入错误", "请输入正确的数字！")


def clear_all():
    number_var.set("")
    combo_multiplier.set("2")
    current_input_var.set("未输入")
    result_value_var.set("结果会显示在这里")
    formula_var.set("公式会显示在这里")

    entry_number.config(fg="black")
    input_value_label.config(fg="black")
    result_value_label.config(fg="black")


# =========================
# 创建主窗口
# =========================
root = tk.Tk()
root.title("除法计算器（颜色分级版）")
root.geometry("620x520")
root.resizable(False, False)
root.configure(bg="#f5f6fa")

# 标题
title_label = tk.Label(
    root,
    text="除法计算器（颜色分级版）",
    font=("Microsoft YaHei", 18, "bold"),
    bg="#f5f6fa",
    fg="#2f3640"
)
title_label.pack(pady=15)

# 输入区域
input_frame = tk.Frame(root, bg="#f5f6fa")
input_frame.pack(pady=8)

tk.Label(
    input_frame,
    text="请输入数字：",
    font=("Microsoft YaHei", 12),
    bg="#f5f6fa"
).grid(row=0, column=0, padx=10, pady=8, sticky="e")

number_var = tk.StringVar()
number_var.trace_add("write", update_input_preview)

entry_number = tk.Entry(
    input_frame,
    textvariable=number_var,
    font=("Microsoft YaHei", 12),
    width=20
)
entry_number.grid(row=0, column=1, padx=10, pady=8)

tk.Label(
    input_frame,
    text="选择倍率：",
    font=("Microsoft YaHei", 12),
    bg="#f5f6fa"
).grid(row=1, column=0, padx=10, pady=8, sticky="e")

combo_multiplier = ttk.Combobox(
    input_frame,
    values=[str(x) for x in OPTIONS],
    font=("Microsoft YaHei", 12),
    width=18,
    state="readonly"
)
combo_multiplier.grid(row=1, column=1, padx=10, pady=8)
combo_multiplier.set("2")

# 按钮区域
button_frame = tk.Frame(root, bg="#f5f6fa")
button_frame.pack(pady=10)

btn_calc = tk.Button(
    button_frame,
    text="开始计算",
    font=("Microsoft YaHei", 11, "bold"),
    bg="#27ae60",
    fg="white",
    width=12,
    command=calculate
)
btn_calc.pack(side=tk.LEFT, padx=10)

btn_clear = tk.Button(
    button_frame,
    text="清空",
    font=("Microsoft YaHei", 11, "bold"),
    bg="#e67e22",
    fg="white",
    width=12,
    command=clear_all
)
btn_clear.pack(side=tk.LEFT, padx=10)

# 输入显示区域
input_show_frame = tk.Frame(root, bg="#ecf0f1", bd=1, relief="solid")
input_show_frame.pack(pady=10, padx=20, fill="x")

tk.Label(
    input_show_frame,
    text="当前输入：",
    font=("Microsoft YaHei", 12),
    bg="#ecf0f1",
    fg="#2c3e50"
).pack(pady=(10, 3))

current_input_var = tk.StringVar(value="未输入")
input_value_label = tk.Label(
    input_show_frame,
    textvariable=current_input_var,
    font=("Microsoft YaHei", 20, "bold"),
    bg="#ecf0f1",
    fg="black"
)
input_value_label.pack(pady=(0, 10))

# 结果显示区域
result_frame = tk.Frame(root, bg="#ecf0f1", bd=1, relief="solid")
result_frame.pack(pady=10, padx=20, fill="x")

tk.Label(
    result_frame,
    text="计算结果：",
    font=("Microsoft YaHei", 12),
    bg="#ecf0f1",
    fg="#2c3e50"
).pack(pady=(10, 3))

result_value_var = tk.StringVar(value="结果会显示在这里")
result_value_label = tk.Label(
    result_frame,
    textvariable=result_value_var,
    font=("Microsoft YaHei", 22, "bold"),
    bg="#ecf0f1",
    fg="black"
)
result_value_label.pack(pady=(0, 8))

formula_var = tk.StringVar(value="公式会显示在这里")
formula_label = tk.Label(
    result_frame,
    textvariable=formula_var,
    font=("Microsoft YaHei", 11),
    bg="#ecf0f1",
    fg="#34495e"
)
formula_label.pack(pady=(0, 12))

# 回车直接计算
root.bind("<Return>", lambda event: calculate())

# 聚焦到输入框
entry_number.focus()

# 启动
root.mainloop()

