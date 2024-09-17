import unittest
from function import Number, Fraction, Expression, CustomMathError

class TestMathFunctions(unittest.TestCase):
    def test_number_initialization(self):
        # Test 1: Initialize Number with max value
        num1 = Number(10)
        self.assertIsInstance(num1, Number)
        self.assertLessEqual(float(num1), 11)  # 检查是否小于等于 11

        # Test 2: Initialize Number with specific values
        num2 = Number(nums=(3, 1, 2))
        self.assertEqual(str(num2), "3'1/2")

        # Test 3: Test invalid initialization
        with self.assertRaises(CustomMathError):
            Number(nums=(1, 2, 0))  # 分母不能为零

    def test_number_reduction(self):
        # Test 4: Reduce fraction
        num = Number(nums=(0, 4, 6))
        num.reduce_fraction()
        self.assertEqual(str(num), "2/3")

    def test_fraction_calculation(self):
        # Test 5: Addition
        f1 = Fraction(Number(nums=(1, 1, 2)), Number(nums=(2, 1, 4)), ' + ')
        result = f1.calculate_fractions()
        self.assertEqual(str(result), "3'3/4")

        # Test 6: Subtraction
        f2 = Fraction(Number(nums=(3, 3, 4)), Number(nums=(1, 1, 2)), ' - ')
        result = f2.calculate_fractions()
        self.assertEqual(str(result), "2'1/4")

        # Test 7: Multiplication
        f3 = Fraction(Number(nums=(2, 1, 2)), Number(nums=(1, 1, 3)), ' * ')
        result = f3.calculate_fractions()
        self.assertEqual(str(result), "3'1/3")

        # Test 8: Division
        f4 = Fraction(Number(nums=(5, 0, 1)), Number(nums=(2, 1, 2)), ' % ')
        result = f4.calculate_fractions()
        self.assertEqual(str(result), "2")

    def test_expression_generation(self):
        # Test 9: Generate expressions
        exp = Expression(10, 5)
        questions, answers = exp.run()
        self.assertEqual(len(questions), 5)
        self.assertEqual(len(answers), 5)

        # Test 10: Check for valid expression format
        for question in questions:
            self.assertRegex(question, r'^[\d\s\+\-\*\%\(\)\'\/]+$')

    def test_error_handling(self):
        # Test 11: Division by zero
        with self.assertRaises(CustomMathError):
            f = Fraction(Number(nums=(1, 0, 1)), Number(nums=(0, 0, 1)), ' % ')
            f.calculate_fractions()

        # Test 12: Positive subtraction (should not raise error)
        f = Fraction(Number(nums=(3, 0, 1)), Number(nums=(2, 0, 1)), ' - ')
        result = f.calculate_fractions()
        self.assertEqual(str(result), "1")



        # Test 13: Zero divided by a number
        f = Fraction(Number(nums=(0, 0, 1)), Number(nums=(5, 0, 1)), ' % ')
        result = f.calculate_fractions()
        self.assertEqual(str(result), "0")

if __name__ == '__main__':
    unittest.main()