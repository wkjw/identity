import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime

# 设置窗口置顶的状态
def toggle_topmost():
    global topmost
    if topmost:
        root.attributes("-topmost", False)
        topmost = False
        pin_button.config(text="置顶")
    else:
        root.attributes("-topmost", True)
        topmost = True
        pin_button.config(text="取消置顶")

# 生成数据的函数
def generate_data():
    try:
        # 清空表格中的数据
        adjust_table_style(15, 35)
        for row in table.get_children():
            table.delete(row)

        num_records = int(num_entry.get())
        male_ratio = gender_scale.get() / 100
        min_age = int(min_age_entry.get())
        max_age = int(max_age_entry.get())
        gender_distribution = [0] * int(num_records * male_ratio) + [1] * (num_records - int(num_records * male_ratio))
        random.shuffle(gender_distribution)

        for i in range(num_records):
            gender = "男" if gender_distribution[i] == 0 else "女"
            age = random.randint(min_age, max_age)
            birth_date = datetime.date.today().replace(month=1, day=1) - datetime.timedelta(days=age*365) + datetime.timedelta(days=random.randint(20, 350))
            if date_format_var.get() == 1:
                birth_date_str = birth_date.strftime("%Y/%m/%d")
            else:
                birth_date_str = birth_date.strftime("%m/%d/%Y")

            # 插入数据并为单双行设置不同的颜色
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            table.insert("", "end", values=(i+1, gender, age, birth_date_str, ""), tags=(tag,))
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的输入。")

    # 生成数据后重新调整底部控制区的位置
    root.update_idletasks()
    bottom_control_frame.lift()

# 性别比例的变化时更新百分比显示
def update_percentage(val):
    male_percentage = int(float(val))
    female_percentage = 100 - male_percentage
    percentage_label.config(text=f"男: {male_percentage}% 女: {female_percentage}%")

# 处理数字输入框输入事件
def handle_number_input(event):
    entry_widget = event.widget
    try:
        value = int(entry_widget.get())
        if value > 99:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, "99")
        elif value < 0:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, "0")
    except ValueError:
        pass

# 处理年龄输入，限制在合法范围内
def handle_age_input(event):
    try:
        value = int(event.widget.get())
        if value > 99:
            event.widget.delete(0, tk.END)
            event.widget.insert(0, "99")
        elif value < 0:
            event.widget.delete(0, tk.END)
            event.widget.insert(0, "0")
    except ValueError:
        pass

# 单击表格单元格进行编辑
def copy_to_clipboard(event):
    selected_item = table.selection()
    if selected_item:
        column_index = table.identify_column(event.x)
        row_id = table.selection()[0]
        col_number = int(column_index.replace('#', '')) - 1

        if col_number == 0 or col_number == 4:  # 允许编辑序号（第 1 列）和备注（第 5 列）
            entry_popup = tk.Entry(root)
            entry_popup.place(x=event.x_root - root.winfo_rootx(), y=event.y_root - root.winfo_rooty())
            entry_popup.insert(0, table.item(selected_item)['values'][col_number])
            entry_popup.focus()

            def save_edit(event=None):
                new_value = entry_popup.get()
                current_values = list(table.item(row_id, "values"))
                current_values[col_number] = new_value
                table.item(row_id, values=current_values)
                entry_popup.destroy()

            entry_popup.bind("<Return>", save_edit)
            entry_popup.bind("<FocusOut>", save_edit)  # 失去焦点时自动保存并关闭

# 日期格式切换时自动更新表格中的日期格式
def update_date_format():
    for row in table.get_children():
        values = table.item(row, "values")
        try:
            if date_format_var.get() == 1:  # 年/月/日
                new_date = datetime.datetime.strptime(values[3], "%m/%d/%Y").strftime("%Y/%m/%d")
            else:  # 月/日/年
                new_date = datetime.datetime.strptime(values[3], "%Y/%m/%d").strftime("%m/%d/%Y")
            values = list(values)
            values[3] = new_date
            table.item(row, values=values)
        except ValueError:
            continue
            
def adjust_table_style(font_size, row_height):
    style.configure("Treeview", font=("Helvetica", font_size), rowheight=row_height)

# 主窗口
root = tk.Tk()
root.title("人设生成器")
root.geometry("850x400")
topmost = False  # 置顶状态

# 设置统一的背景颜色和字体颜色
background_color = '#5B618A'
font_color = '#FFFFFF'

root.configure(bg=background_color)

# 调整字体大小和颜色
default_font = ("Helvetica", 14)

# 创建一个 ttk.Style 实例并设置 Treeview 的字体和外观
style = ttk.Style()
style.configure("Treeview", font=default_font, rowheight=30)  
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))  
style.map("Treeview.Heading", foreground=[('active', background_color), ('!active', background_color)])
style.configure("TFrame", background=background_color)  
style.configure("TLabel", foreground=font_color)  
style.configure("TEntry", foreground=background_color)  
style.configure("TScale", foreground=font_color)  
style.configure("TButton", foreground=background_color)  
style.configure("TRadiobutton", foreground=font_color)  
style.configure("TLabel", background=background_color)  
style.configure("TScale", background=background_color)   
style.configure("TRadiobutton", background=background_color)  


# 整体布局框架
main_frame = ttk.Frame(root, style="TFrame")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 左部控制区框架
left_control_frame = ttk.Frame(main_frame, style="TFrame")
left_control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# 记录数量
ttk.Label(left_control_frame, text="生成数量：", font=default_font, style="TLabel").pack(pady=5)
num_entry = ttk.Entry(left_control_frame, width=5, font=default_font, style="TEntry")
num_entry.delete(0, tk.END)
num_entry.insert(0, "20")
num_entry.pack(pady=5)
num_entry.bind("<KeyRelease>", handle_number_input)

# 性别比例
percentage_label = ttk.Label(left_control_frame, text="男: 50% 女: 50%", font=default_font, style="TLabel")
percentage_label.pack(pady=5)

ttk.Label(left_control_frame, text="性别比例：", font=default_font, style="TLabel").pack(pady=5)
gender_scale = ttk.Scale(left_control_frame, from_=0, to=100, orient="horizontal", length=200, command=update_percentage, style="TScale")
gender_scale.set(50)
gender_scale.pack(pady=5)

# 年龄范围一行显示
age_frame = ttk.Frame(left_control_frame, style="TFrame")
age_frame.pack(pady=5)
ttk.Label(age_frame, text="年龄范围：", font=default_font, style="TLabel").pack(side=tk.LEFT)
min_age_entry = ttk.Entry(age_frame, width=5, font=default_font, style="TEntry")
min_age_entry.pack(side=tk.LEFT)
min_age_entry.insert(0,"18")
min_age_entry.bind("<KeyRelease>", handle_age_input)
ttk.Label(age_frame, text="到", font=default_font, style="TLabel").pack(side=tk.LEFT)
max_age_entry = ttk.Entry(age_frame, width=5, font=default_font, style="TEntry")
max_age_entry.pack(side=tk.LEFT)
max_age_entry.insert(0,"60")
max_age_entry.bind("<KeyRelease>", handle_age_input)

# 生成按钮
generate_button = ttk.Button(left_control_frame, text="生成", command=generate_data, style="TButton")
generate_button.pack(pady=10)

# 右部表格区框架
right_table_frame = ttk.Frame(main_frame, style="TFrame")
right_table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 创建一个带有边框的框架来包含表格
table_container = ttk.Frame(right_table_frame, borderwidth=2, relief="solid", style="TFrame")
table_container.pack(fill=tk.BOTH, expand=True)

# 表格列（增加序号和备注列）
columns = ("序号", "性别", "年龄", "出生日期", "备注")
table = ttk.Treeview(table_container, columns=columns, show="headings", height=20)

# 设置表格列标题
for col in columns:
    table.heading(col, text=col)

# 调整列宽度
table.column("序号", width=80)
table.column("性别", width=50)
table.column("年龄", width=50)
table.column("出生日期", width=150)
table.column("备注", width=200)

# 为单双行添加不同的颜色
#table.tag_configure('evenrow', background='#E8E8E8')
table.tag_configure('oddrow', background='#C3CBDC')

table.pack(fill=tk.BOTH, expand=True)

# 绑定双击事件进行编辑
table.bind("<Double-1>", copy_to_clipboard)

# 自适应列宽度
for col in columns:
    table.column(col, anchor="center", stretch=True)

# 底部控制区框架
bottom_control_frame = ttk.Frame(left_control_frame, style="TFrame")
bottom_control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# 日期格式选择
date_format_var = tk.IntVar(value=1)
ttk.Radiobutton(bottom_control_frame, text="年/月/日", variable=date_format_var, value=1, command=update_date_format, style="TRadiobutton").pack(side=tk.LEFT, padx=10)
ttk.Radiobutton(bottom_control_frame, text="月/日/年", variable=date_format_var, value=2, command=update_date_format, style="TRadiobutton").pack(side=tk.LEFT, padx=10)

# 置顶按钮
pin_button = ttk.Button(bottom_control_frame, text="置顶", command=toggle_topmost, style="TButton")
pin_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()