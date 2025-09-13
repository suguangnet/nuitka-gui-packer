import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class GUIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Nuitka打包工具")
        # 设置窗口宽度和高度
        window_width = 600
        window_height = 630
        # 获取屏幕宽度和高度
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # 计算窗口左上角坐标使其居中
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        # 设置窗口大小和位置
        master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # 创建选择输出目录的按钮
        self.output_dir_button = tk.Button(master, text="选择输出目录", command=self.choose_output_dir)
        self.output_dir_button.pack()
        # 显示选择的输出目录路径
        self.output_dir_label = tk.Label(master, text="")
        self.output_dir_label.pack()
        
        # 创建选择.py文件的按钮
        self.main_file_button = tk.Button(master, text="选择.py文件", command=self.choose_main_file)
        self.main_file_button.pack()
        # 显示选择的.py文件路径
        self.main_file_label = tk.Label(master, text="")
        self.main_file_label.pack()
        
        # 创建选择.icon图标的按钮
        self.icon_file_button = tk.Button(master, text="选择.icon图标", command=self.choose_icon_file)
        self.icon_file_button.pack()
        # 显示选择的.icon图标路径
        self.icon_file_label = tk.Label(master, text="")
        self.icon_file_label.pack()
        
        # 创建输入框
        self.entry_label = tk.Label(master, text="请输入Nuitka --enable-plugin参数，多个用逗号隔开，可以为空")
        self.entry_label.pack()
        # 创建输入框，并设置默认值为 "tk-inter"
        self.entry = tk.Entry(master, width=50)
        self.entry.insert(0, "tk-inter")
        self.entry.pack()
        
        # 创建按钮
        self.pack_button = tk.Button(master, text="编译开始", command=self.pack_and_run)
        self.pack_button.pack(pady=20)
        
        # 注：安装Nuitka和GCC（配置环境变量）
        self.developer_label = tk.Label(master, text="注：安装Nuitka和GCC（配置环境变量）,输出目录不选择则会输出到.py同目录下")
        self.developer_label.pack(side="top", pady=5)
        
        # 创建 Text 组件，用于显示进度
        self.progress_text = tk.Text(master, height=20, width=80)
        self.progress_text.pack()
        
        # 初始化选择的文件路径
        self.output_dir = ""
        self.main_file = ""
        self.icon_file = ""
        
        # 在窗口底部添加 "Development by 速光网络-都百顺" 横向居中显示
        self.developer_label = tk.Label(master, text="Development by 速光网络-都百顺（抖音号：dubaishun12）")
        self.developer_label.pack(side="bottom", pady=20)
    
    def choose_output_dir(self):
        selected_dir = filedialog.askdirectory(title="选择输出目录")
        if selected_dir:
            self.output_dir = selected_dir
            self.output_dir_label.config(text=f"选择的输出目录: {self.output_dir}")
        else:
            self.output_dir = ""
            self.output_dir_label.config(text="选择的输出目录: 未选择")
    
    def choose_main_file(self):
        selected_file = filedialog.askopenfilename(title="选择.py文件", filetypes=[("Python files", "*.py")])
        if selected_file:
            self.main_file = selected_file
            self.main_file_label.config(text=f"选择的.py文件: {self.main_file}")
        else:
            self.main_file = ""
            self.main_file_label.config(text="选择的.py文件: 未选择")
    
    def choose_icon_file(self):
        selected_icon_file = filedialog.askopenfilename(title="选择.icon图标", filetypes=[("Icon files", "*.ico")])
        if selected_icon_file:
            self.icon_file = selected_icon_file
            self.icon_file_label.config(text=f"选择的.icon图标: {self.icon_file}")
        else:
            self.icon_file = ""
            self.icon_file_label.config(text="选择的.icon图标: 未选择")
    
    def pack_and_run(self):
        # 检查是否选择了主文件
        if not self.main_file:
            messagebox.showerror("错误", "请先选择要编译的.py文件")
            return
        
        # 获取输入的 Nuitka 参数
        nuitka_params = self.entry.get()
        
        # 检查是否选择了输出目录，如果没有，使用 .py 文件的目录
        if not self.output_dir:
            self.output_dir = os.path.dirname(self.main_file)
        
        # 构建命令列表
        command = [
            "python", "-m", "nuitka",
            "--onefile", "--show-progress", "--remove-output", "--windows-disable-console",
            f"--output-dir={self.output_dir}", self.main_file,
        ]
        
        # 如果选择了 .icon 文件，则添加相应参数
        if self.icon_file:
            command.append(f"--windows-icon-from-ico={self.icon_file}")
        
        # 如果手工输入了 --enable-plugin 参数，则添加相应参数
        if nuitka_params:
            command.append(f"--enable-plugin={nuitka_params}")
        
        try:
            # 清空进度文本框
            self.progress_text.delete(1.0, tk.END)
            
            # 使用 subprocess.Popen 启动 CMD 窗口并捕获输出
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
            
            # 读取并显示输出
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                self.progress_text.insert(tk.END, output)
                self.progress_text.see(tk.END)
                self.progress_text.update_idletasks()
            
            # 检查进程是否成功完成
            if process.returncode == 0:
                # 如果进程成功完成，显示成功消息
                messagebox.showinfo("成功", "编译成功！")
            else:
                # 如果进程失败，显示错误消息
                messagebox.showerror("错误", f"编译失败，错误代码: {process.returncode}")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()