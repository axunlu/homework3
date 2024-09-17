# function.py
# 定义数学相关功能的文件

import random
import math


class CustomMathError(Exception):
    """自定义数学错误类，用于处理特定的数学相关异常"""
    pass


class Number:
    def __init__(self, max: int = None, nums: tuple = None):
        """
        初始化一个Number对象
        :param max: 随机生成数字时的最大值
        :param nums: 用于直接指定数字的组成部分（整数，分子，分母）
        """
        try:
            if nums:
                # 如果提供了nums元组，直接用它来初始化数字
                if isinstance(nums, tuple) and len(nums) == 3:
                    if nums[2] == 0:
                        raise ValueError("分母不能为零。")
                    else:
                        self.integer = int(nums[0])  # 整数部分
                        self.numerator = int(nums[1])  # 分子
                        self.denominator = int(nums[2])  # 分母
                else:
                    raise ValueError("nums必须是一个三元组（整数，分子，分母）。")
            else:
                # 如果没有提供nums，则随机生成一个数字
                if (not isinstance(max, int)) or max < 1:
                    raise ValueError("max必须大于等于1。")
                self.integer = random.randint(0, max - 1)  # 随机生成整数部分
                self.denominator = random.randint(1, max - 1)  # 随机生成分母
                is_fra = random.randint(1, 2)  # 随机决定是否生成分数部分
                if is_fra == 1:
                    self.numerator = random.randint(1, self.denominator)  # 生成分子
                else:
                    self.numerator = 0  # 不生成分数部分
                    # 计算生成的数值
                generated_value = self.integer + self.numerator / self.denominator
                # 如果生成的值大于等于 max，调整整数部分使其小于 max
                if generated_value >= max:
                    adjustment = int(generated_value // max)
                    self.integer -= adjustment
        except ValueError as e:
            raise CustomMathError(str(e))

    def reduce_fraction(self):
        """简化分数"""
        # 计算最大公约数
        gcd = math.gcd(self.numerator, self.denominator)
        numerator = self.numerator // gcd
        denominator = self.denominator // gcd
        # 处理假分数，将其转化为带分数
        integer = numerator // denominator + self.integer
        numerator = numerator % denominator
        self.integer = int(integer)
        self.numerator = int(numerator)
        self.denominator = int(denominator)

    def __str__(self):
        """将Number对象转换为字符串表示"""
        if self.integer == 0:
            if self.numerator:
                return f"{self.numerator}/{self.denominator}"
            else:
                return '0'
        else:
            if self.numerator:
                return f"{self.integer}'{self.numerator}/{self.denominator}"
            else:
                return str(self.integer)

    def __float__(self):
        """将Number对象转换为浮点数"""
        return self.integer + self.numerator / self.denominator


class Fraction:
    def __init__(self, f1: Number, f2: Number, op: str):
        """
        初始化一个Fraction对象，表示两个Number对象之间的运算
        :param f1: 第一个Number对象
        :param f2: 第二个Number对象
        :param op: 运算符
        """
        if isinstance(f1, Number) and isinstance(f2, Number):
            self.f1 = f1
            self.f2 = f2
        else:
            raise CustomMathError("参数必须是Number类型。")
        if op in [' + ', ' - ', ' * ', ' % ']:
            self.op = op
        else:
            raise CustomMathError("操作符必须是' + ', ' - ', ' * ', 或 ' % '之一。")

    def calculate_fractions(self):
        """执行分数计算"""
        try:
            if self.op == ' + ':
                # 加法运算
                denominator = self.f1.denominator * self.f2.denominator
                numerator = (self.f1.integer * self.f1.denominator + self.f1.numerator) * self.f2.denominator \
                            + (self.f2.integer * self.f2.denominator + self.f2.numerator) * self.f1.denominator
                result = Number(nums=(0, numerator, denominator))
            elif self.op == ' - ':
                # 减法运算
                denominator = self.f1.denominator * self.f2.denominator
                numerator = (self.f1.integer * self.f1.denominator + self.f1.numerator) * self.f2.denominator \
                            - (self.f2.integer * self.f2.denominator + self.f2.numerator) * self.f1.denominator
                result = Number(nums=(0, numerator, denominator))
            elif self.op == ' * ':
                # 乘法运算
                denominator = self.f1.denominator * self.f2.denominator
                numerator = (self.f1.numerator + self.f1.integer * self.f1.denominator) \
                            * (self.f2.numerator + self.f2.integer * self.f2.denominator)
                result = Number(nums=(0, numerator, denominator))
            elif self.op == ' % ':
                # 除法运算
                if float(self.f2) == 0:
                    raise CustomMathError("除数不能为零。")
                denominator = self.f1.denominator * (self.f2.numerator + self.f2.integer * self.f2.denominator)
                numerator = (self.f1.numerator + self.f1.integer * self.f1.denominator) * self.f2.denominator
                result = Number(nums=(0, numerator, denominator))

            result.reduce_fraction()  # 简化结果
            return result
        except OverflowError:
            raise CustomMathError("计算结果超出可表示范围")


class Expression:
    def __init__(self, max, question_num):
        """
        初始化一个Expression对象
        :param max: 生成数字的最大值
        :param question_num: 要生成的问题数量
        """
        self.max = max
        self.question_num = question_num
        self.expressions = set()  # 用于存储生成的表达式字符串，确保不重复
        self.expression_lists = []  # 存储生成的表达式列表
        self.generation_times = 0  # 记录生成表达式的尝试次数
        self.answers = []  # 存储计算得到的答案
        self.questions = []  # 存储最终生成的问题
        self.expression_num = 0  # 当前已生成的有效表达式数量

    def generate_subexpression(self, etype, op):
        """
        生成子表达式
        :param etype: 表达式类型（1表示二元运算，2表示一元运算）
        :param op: 运算符
        """
        if etype == 1:
            # 生成两个随机数
            num_1 = Number(self.max)
            num_1.reduce_fraction()
            num_2 = Number(self.max)
            num_2.reduce_fraction()
            if op != ' % ':
                # 非除法运算时，确保大数在前
                if float(num_1) >= float(num_2):
                    subexpression = [num_1, op, num_2]
                else:
                    subexpression = [num_2, op, num_1]
            else:
                subexpression = [num_1, op, num_2]
        else:
            # 生成一元运算表达式
            if op in [' - ', ' % ']:
                if random.randint(0, 1):
                    num = Number(self.max)
                    num.reduce_fraction()
                    subexpression = [op, num]
                else:
                    num = Number(self.max)
                    num.reduce_fraction()
                    subexpression = [num, op]
            else:
                num = Number(self.max)
                num.reduce_fraction()
                subexpression = [op, num]
        return subexpression

    def generate_expression_list(self):
        """生成表达式列表"""
        expression_list = []
        sub_num = random.randint(1, 3)  # 随机决定子表达式的数量
        operators = [random.choice([' + ', ' - ', ' * ', ' % ']) for _ in range(sub_num)]
        subexpression_1 = self.generate_subexpression(1, operators[0])
        str_sub_1 = str(subexpression_1[0]) + subexpression_1[1] + str(subexpression_1[2])
        if sub_num == 1:
            expression_list.append(subexpression_1)
            str_sub_2 = ''
            str_sub_3 = ''
            string = str_sub_1 + '|' + str_sub_2 + '|' + str_sub_3
        elif sub_num == 2:
            subexpression_2 = self.generate_subexpression(2, operators[1])
            str_sub_2 = str(subexpression_2[0]) + str(subexpression_2[1])
            str_sub_3 = ''
            expression_list.append(subexpression_1)
            expression_list.append(subexpression_2)
            string = str_sub_1 + '|' + str_sub_2 + '|' + str_sub_3
        else:
            etype = random.randint(1, 2)
            subexpression_2 = self.generate_subexpression(etype, operators[1])
            if etype == 1:
                subexpression_3 = [operators[2]]
                str_sub_2 = str(subexpression_2[0]) + str(subexpression_2[1]) + str(subexpression_2[2])
                str_sub_3 = subexpression_3[0]
                if str_sub_1 >= str_sub_2 and operators[2] in [' + ', ' * ']:
                    expression_list.append(subexpression_1)
                    expression_list.append(subexpression_2)
                    expression_list.append(subexpression_3)
                    string = str_sub_1 + '|' + str_sub_2 + '|' + str_sub_3
                else:
                    expression_list.append(subexpression_2)
                    expression_list.append(subexpression_1)
                    expression_list.append(subexpression_3)
                    string = str_sub_1 + '|' + str_sub_2 + '|' + str_sub_3
            else:
                subexpression_3 = self.generate_subexpression(2, operators[2])
                str_sub_2 = str(subexpression_2[0]) + str(subexpression_2[1])
                str_sub_3 = str(subexpression_3[0]) + str(subexpression_3[1])
                expression_list.append(subexpression_1)
                expression_list.append(subexpression_2)
                expression_list.append(subexpression_3)
                string = str_sub_1 + '|' + str_sub_2 + '|' + str_sub_3
        return expression_list, string

    def calculate_answer(self, expression_list):
        """
        计算表达式的答案
        :param expression_list: 表达式列表
        """
        try:
            # 计算第一个子表达式的结果
            expression_1 = Fraction(expression_list[0][0], expression_list[0][2], expression_list[0][1])
            result_1 = expression_1.calculate_fractions()
            if float(result_1) < 0:
                raise CustomMathError("子表达式不能小于零。")
            if len(expression_list) == 1:
                result = result_1
            elif len(expression_list) == 2:
                # 处理两个子表达式的情况
                if isinstance(expression_list[1][0], str):
                    expression_2 = Fraction(result_1, expression_list[1][1], expression_list[1][0])
                else:
                    expression_2 = Fraction(expression_list[1][0], result_1, expression_list[1][1])
                result = expression_2.calculate_fractions()
            else:
                # 处理三个子表达式的情况
                if len(expression_list[2]) == 1:
                    expression_2 = Fraction(expression_list[1][0], expression_list[1][2], expression_list[1][1])
                    result_2 = expression_2.calculate_fractions()
                    if float(result_2) < 0:
                        raise CustomMathError("子表达式不能小于零。")
                    expression_3 = Fraction(result_1, result_2, expression_list[2][0])
                    result = expression_3.calculate_fractions()
                else:
                    if isinstance(expression_list[1][0], str):
                        expression_2 = Fraction(result_1, expression_list[1][1], expression_list[1][0])
                    else:
                        expression_2 = Fraction(expression_list[1][0], result_1, expression_list[1][1])
                    result_2 = expression_2.calculate_fractions()
                    if float(result_2) < 0:
                        raise CustomMathError("子表达式不能小于零。")
                    if isinstance(expression_list[2][0], str):
                        expression_2 = Fraction(result_2, expression_list[2][1], expression_list[2][0])
                    else:
                        expression_2 = Fraction(expression_list[2][0], result_2, expression_list[2][1])
                    result = expression_2.calculate_fractions()
            if float(result) < 0:
                raise CustomMathError("子表达式不能小于零。")
            return result
        except CustomMathError as e:
            raise e
        except Exception:
            raise CustomMathError("计算过程中出现错误。")

    def generate_expressions(self):
        """生成表达式"""
        while self.expression_num < self.question_num:
            self.generation_times += 1
            try:
                exp_list, exp_string = self.generate_expression_list()
                answer = self.calculate_answer(exp_list)
            except CustomMathError:
                continue  # 如果生成的表达式无效，则继续尝试
            self.expressions.add(exp_string)  # 添加到已生成的表达式集合中
            self.expression_lists.append(exp_list)
            self.answers.append(str(answer))
            self.expression_num += 1

    def randomly_generate_questions(self):
        """随机生成问题"""
        for expression in self.expression_lists:
            op_1 = expression[0][1]  # 第一个操作符
            # 处理第一个子表达式
            if expression[0][1] in [' + ', ' * ']:
                if random.randint(0, 1):
                    question_1 = str(expression[0][0]) + str(expression[0][1]) + str(expression[0][2])
                else:
                    question_1 = str(expression[0][2]) + str(expression[0][1]) + str(expression[0][0])
            else:
                question_1 = str(expression[0][0]) + str(expression[0][1]) + str(expression[0][2])

            if len(expression) >= 2:
                # 处理第二个子表达式
                if len(expression[1]) == 2:
                    if str(expression[1][0]) == ' + ':
                        op_2 = ' + '
                        if random.randint(0, 1):
                            question_2 = question_1 + op_2 + str(expression[1][1])
                        else:
                            if expression[0][1] in [' + ', ' - ']:
                                question_2 = str(expression[1][1]) + op_2 + '(' + question_1 + ')'
                            else:
                                question_2 = str(expression[1][1]) + op_2 + question_1
                    elif str(expression[1][0]) == ' * ':
                        op_2 = ' * '
                        if random.randint(0, 1):
                            if str(expression[0][1]) in [' * ', ' % ']:
                                question_2 = question_1 + op_2 + str(expression[1][1])
                            else:
                                question_2 = '(' + question_1 + ')' + op_2 + str(expression[1][1])
                        else:
                            question_2 = str(expression[1][1]) + op_2 + '(' + question_1 + ')'
                    elif str(expression[1][0]) == ' - ':
                        op_2 = ' - '
                        question_2 = question_1 + op_2 + str(expression[1][1])
                    elif str(expression[1][0]) == ' % ':
                        op_2 = ' % '
                        if str(expression[0][1]) in [' * ', ' % ']:
                            question_2 = question_1 + op_2 + str(expression[1][1])
                        else:
                            question_2 = '(' + question_1 + ')' + op_2 + str(expression[1][1])
                    elif str(expression[1][1]) == ' - ':
                        op_2 = ' - '
                        if str(expression[0][1]) in [' * ', ' % ']:
                            question_2 = str(expression[1][0]) + op_2 + question_1
                        else:
                            question_2 = str(expression[1][0]) + op_2 + '(' + question_1 + ')'
                    else:
                        op_2 = ' % '
                        question_2 = str(expression[1][0]) + op_2 + '(' + question_1 + ')'

                    # 处理第三个子表达式（如果存在）
                    if len(expression) > 2:
                        if expression[2][0] == ' + ':
                            op_3 = ' + '
                            if random.randint(0, 1):
                                question_3 = question_2 + op_3 + str(expression[2][1])
                            else:
                                if op_1 in [' + ', ' - '] and op_2 in [' + ', ' - ']:
                                    question_3 = str(expression[2][1]) + op_3 + '(' + question_2 + ')'
                                else:
                                    question_3 = str(expression[2][1]) + op_3 + question_2
                        elif expression[2][0] == ' - ':
                            op_3 = ' - '
                            question_3 = question_2 + op_3 + str(expression[2][1])
                        elif expression[2][0] == ' * ':
                            op_3 = ' * '
                            if random.randint(0, 1):
                                question_3 = str(expression[2][1]) + op_3 + '(' + question_2 + ')'
                            else:
                                if op_2 in [' * ', ' % ']:
                                    question_3 = question_2 + op_3 + str(expression[2][1])
                                else:
                                    question_3 = '(' + question_2 + ')' + op_3 + str(expression[2][1])
                        elif expression[2][0] == ' % ':
                            op_3 = ' % '
                            if op_2 in [' * ', ' % ']:
                                question_3 = question_2 + op_3 + str(expression[2][1])
                            else:
                                question_3 = '(' + question_2 + ')' + op_3 + str(expression[2][1])
                        elif expression[2][1] == ' - ':
                            op_3 = ' - '
                            if op_2 in [' * ', ' % ']:
                                question_3 = str(expression[2][0]) + op_3 + question_2
                            else:
                                question_3 = str(expression[2][0]) + op_3 + '(' + question_2 + ')'
                        elif expression[2][1] == ' % ':
                            op_3 = ' % '
                            question_3 = str(expression[2][0]) + op_3 + '(' + question_2 + ')'
                else:
                    # 处理第二个子表达式为完整表达式的情况
                    question_1 = '(' + question_1 + ')'
                    question_2 = '(' + str(expression[1][0]) + str(expression[1][1]) + str(expression[1][2]) + ')'
                    if str(expression[2][0]) in [' + ', ' * ']:
                        if random.randint(0, 1):
                            question_3 = question_1 + str(expression[2][0]) + question_2
                        else:
                            question_3 = question_2 + str(expression[2][0]) + question_1
                    else:
                        question_3 = question_2 + str(expression[2][0]) + question_1

            # 根据子表达式的数量，将最终的问题添加到问题列表中
            if len(expression) == 1:
                self.questions.append(question_1)
            elif len(expression) == 2:
                self.questions.append(question_2)
            else:
                self.questions.append(question_3)

    def run(self):
        """运行表达式生成过程"""
        self.generate_expressions()  # 生成表达式
        self.randomly_generate_questions()  # 随机生成问题
        return self.questions, self.answers  # 返回生成的问题和答案


# 测试代码
if __name__ == "__main__":
    try:
        # 创建一个Expression对象，设置最大值为10，生成5个问题
        exp = Expression(10, 5)
        # 运行表达式生成过程
        questions, answers = exp.run()
        # 打印生成的问题和答案
        for q, a in zip(questions, answers):
            print(f"问题: {q}")
            print(f"答案: {a}")
            print()
    except CustomMathError as e:
        print(f"发生错误: {e}")
