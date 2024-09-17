# main.py
# 主程序入口文件
# 2024-09-16完成
from interface import *     # 导入interface模块中的所有内容

# 主函数
if __name__ == "__main__":
    root = tk.Tk()          # 创建Tkinter根窗口
    app = MathQuizApp(root)      # 创建MathQuizApp实例，并将根窗口作为参数传递
    root.mainloop()             # 进入Tkinter事件循环
