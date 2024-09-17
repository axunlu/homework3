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
