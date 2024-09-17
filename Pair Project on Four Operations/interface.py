import tkinter as tk
from function import *
from PIL import Image, ImageTk, ImageEnhance
import re


class MathQuizApp:
    def __init__(self, root):
        """ 初始化 MathQuizApp 类 """
        self.root = root
        self.root.title("四则运算题目生成器")

        # 调用封装的初始化方法
        self.setup_background()
        self.setup_widgets()

    def setup_background(self):
        """ 设置背景图片和Canvas """
        # 加载并调整背景图片
        background_image = Image.open("background.png")
        background_image = background_image.resize((700, 700), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Brightness(background_image)  # 调整亮度
        background_image = enhancer.enhance(0.8)
        self.background_photo = ImageTk.PhotoImage(background_image)

        # 创建Canvas组件用于显示背景
        self.canvas = tk.Canvas(self.root, width=700, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

    def setup_widgets(self):
        """ 初始化界面控件 """
        # 创建题目数量和最大值的输入框
        self.num_questions_label = self.create_label("题目数量:", 350, 50)
        self.num_questions_entry = self.create_entry(350, 80)
        self.max_value_label = self.create_label("最大值:", 350, 120)
        self.max_value_entry = self.create_entry(350, 150)

        # 创建生成题目按钮
        self.generate_button = self.create_button("开始生成题目", self.generate_questions, 350, 190)

        # 创建题目和答案显示区域
        self.questions_label = self.create_label("题目:", 350, 240)
        self.questions_text = self.create_text_area(350, 280, 10, 40)
        self.answers_label = self.create_label("答案:", 350, 420)
        self.answers_text = self.create_text_area(350, 460, 10, 40)

        # 创建提交答案按钮
        self.submit_button = self.create_button("提交答案", self.check_answers, 350, 510)

        # 创建答题结果显示区域
        self.results_label = self.create_label("答题结果:", 350, 550)
        self.results_text = self.create_text_area(350, 590, 5, 40)

    def create_label(self, text, x, y):
        """ 创建一个Label并放置在Canvas上 """
        label = tk.Label(self.root, text=text, bg='white')
        self.canvas.create_window(x, y, window=label)
        return label

    def create_entry(self, x, y):
        """ 创建一个Entry并放置在Canvas上 """
        entry = tk.Entry(self.root)
        self.canvas.create_window(x, y, window=entry)
        return entry

    def create_button(self, text, command, x, y):
        """ 创建一个Button并放置在Canvas上 """
        button = tk.Button(self.root, text=text, command=command)
        self.canvas.create_window(x, y, window=button)
        return button

    def create_text_area(self, x, y, height, width):
        """ 创建一个Text区域并放置在Canvas上 """
        text_area = tk.Text(self.root, height=height, width=width)
        self.canvas.create_window(x, y, window=text_area)
        return text_area

    def generate_questions(self):
        """ 生成数学题目 """
        try:
            # 获取用户输入的题目数量和最大值
            num_questions = self.validate_input(self.num_questions_entry.get())
            max_value = self.validate_input(self.max_value_entry.get())

            # 调用 function.py 中的 Expression 类生成题目
            exp = Expression(max_value, num_questions)
            self.questions, self.answers = exp.run()

            # 清空文本框并显示生成的题目
            self.questions_text.delete(1.0, tk.END)
            self.answers_text.delete(1.0, tk.END)
            for i, question in enumerate(self.questions, start=1):
                self.questions_text.insert(tk.END, f"{i}. {question}\n")

            # 将题目和答案保存到文件
            with open("Exercises.txt", "w") as question_file:
                question_file.writelines(f"{q}\n" for q in self.questions)
            with open("Answer.txt", "w") as answer_file:
                answer_file.writelines(f"{a}\n" for a in self.answers)

        except ValueError as e:
            # 显示错误消息
            self.show_error(str(e))

    def validate_input(self, value):
        """ 验证用户输入是否为有效的正整数 """
        # 移除所有空白字符
        value = re.sub(r'\s', '', value)
        # 检查是否为正整数
        if not value.isdigit() or int(value) <= 0:
            raise ValueError("请输入有效的正整数")
        return int(value)

    def show_error(self, message):
        """ 显示错误消息 """
        error_window = tk.Toplevel(self.root)
        error_window.title("输入错误")
        error_label = tk.Label(error_window, text=message, padx=20, pady=20)
        error_label.pack()
        ok_button = tk.Button(error_window, text="确定", command=error_window.destroy)
        ok_button.pack(pady=10)

    def check_answers(self):
        """ 检查用户输入的答案 """
        # 获取用户输入的答案
        user_answers = self.answers_text.get(1.0, tk.END).splitlines()

        # 初始化正确和错误的题目列表
        correct = []
        incorrect = []

        # 比较答案
        for i, (user_answer, correct_answer) in enumerate(zip(user_answers, self.answers), start=1):
            if user_answer.strip() == correct_answer.strip():
                correct.append(i)
            else:
                incorrect.append(i)

        # 显示结果
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"正确题号: {', '.join(map(str, correct))}\n")
        self.results_text.insert(tk.END, f"错误题号: {', '.join(map(str, incorrect))}\n")

        # 保存结果到文件
        with open("Grade.txt", "w") as grade_file:
            grade_file.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
            grade_file.write(f"Wrong: {len(incorrect)} ({', '.join(map(str, incorrect))})\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
