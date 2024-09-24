import random
import fractions
import argparse
import os
import re


# 生成四则运算表达式
def generate_expression(max_value, max_operators):
    '''
    operators = ['+', '-', '*', '/']
    # 初始化一个空字符串，用于构建算术表达式
    expression = ""
    # 随机选择一个运算符的数量，这个数量不会超过max_operators
    num_operators = random.randint(2, max_operators)

    # 循环num_operators次，每次循环都向表达式中添加一个运算符和一个数值（整数或分数）
    for i in range(num_operators):
        # 如果不是第一个运算符，在运算符前添加一个空格
        if i > 0:
            current_operator = random.choice(operators)
            expression += " " + current_operator + " "
        # 随机选择是添加一个整数还是分数
        if random.choice([True, False]):
            # 随机选择分子和分母，确保分子小于分母以得到一个真分数
            numerator = random.randint(1, max_value)
            denominator = random.randint(1, max_value)
            # 如果分子大于或等于分母，重新选择分子和分母
            while numerator >= denominator:
                numerator = random.randint(1, max_value)
                denominator = random.randint(1, max_value)
            expression += str(numerator) + "/" + str(denominator)
        else:
            # 如果是减法，确保右侧的数值小于左侧的数值
            if current_operator == '-':
                value = random.randint(1, max_value)
                expression += str(value)
            else:
                value = random.randint(1, max_value)
                expression += str(value)

    return expression
    '''

    operators = ['+', '-', '*', '/']
    expression = ""

    # 初始化第一个操作数
    first_value = random.choice([random.randint(1, max_value), choose_proper_fraction(max_value)])
    expression += str(first_value)

    num_operators = random.randint(2, max_operators)

    for i in range(1, num_operators):
        # 为下一个操作符选择一个操作数
        next_value = random.choice([random.randint(1, max_value), choose_proper_fraction(max_value)])

        # 随机选择一个操作符
        current_operator = random.choice(operators)
        # 如果是减法，确保被减数大于等于减数
        if current_operator == '-':
            while isinstance(first_value, int) and isinstance(next_value, int) and first_value < next_value:
                next_value = random.randint(1, max_value)
            expression += " - " + str(next_value)
        elif current_operator == '+':
            expression += " + " + str(next_value)
        elif current_operator == '*':
            expression += " * " + str(next_value)
        elif current_operator == '/':
            # 确保除数不为0
            while isinstance(next_value, int) and (next_value == 0):
                next_value = random.randint(1, max_value)
            expression += " / " + str(next_value)

        # 更新 first_value 为当前表达式的值
        # 注意：对于减法和除法，我们需要根据操作结果更新 first_value
        if current_operator == '-' or current_operator == '/':
            if isinstance(first_value, int) and isinstance(next_value, int):
                first_value = first_value - next_value if current_operator == '-' else first_value // next_value
            else:
                # 这里我们简化处理，假设分数操作后仍然是分数，不进行实际计算
                first_value = f"({expression})"
        else:
            first_value = next_value

    return expression

# 生成真分数
def choose_proper_fraction(max_value):
    numerator = random.randint(1, max_value - 1)
    denominator = random.randint(numerator + 1, max_value)
    return f"{numerator}/{denominator}"

# 计算表达式的值
def calculate_expression(expression):
    '''
    try:
        # 使用Python内置的eval函数来计算字符串形式的算术表达式
        # eval函数将字符串视为有效的Python表达式，并执行它
        return eval(expression)
    except ZeroDivisionError:
        # 如果在计算过程中出现除以零的错误（ZeroDivisionError）
        # 捕获这个异常，并返回字符串"Error"
        return "Error"
    '''
    try:
        # 使用eval函数计算表达式的值
        result = eval(expression)

        # 将结果转换为分数
        fraction_result = fractions.Fraction(result).limit_denominator()

        # 将分数转换为字符串
        if fraction_result.denominator == 1:
            # 如果分母为1，则结果为整数
            return str(fraction_result.numerator)
        else:
            # 如果分子大于分母，则转换为带分数形式
            if fraction_result.numerator >= fraction_result.denominator:
                whole_number = fraction_result.numerator // fraction_result.denominator
                remainder = fraction_result.numerator % fraction_result.denominator
                if remainder == 0:
                    # 如果没有余数，则只返回整数部分
                    return str(whole_number)
                else:
                    # 如果有余数，则返回带分数形式
                    return f"{whole_number}'{remainder}/{fraction_result.denominator}"
            else:
                # 如果是真分数，则直接返回分数形式
                return f"{fraction_result.numerator}/{fraction_result.denominator}"
    # 如果在计算过程中出现除以零的错误（ZeroDivisionError）
    # 捕获这个异常，并返回字符串"Error"
    except ZeroDivisionError:
        return "Error"
# 检查题目是否重复
#两个参数：expression（要检查的算术表达式）和existing_expressions（已有的表达式集合）
def is_duplicate(expression, existing_expressions):
    # 遍历一个包含加法、乘法和除法运算符的列表
    for op in ['+', '*', '/']:
        # 使用字符串的replace方法将当前运算符从表达式中移除
        expression = expression.replace(op, '')
    # 在删除了指定的运算符之后，检查修改后的表达式是否存在于existing_expressions集合中
    # 如果存在，则说明有相同数字顺序的题目已经存在（不考虑运算符），返回True
    # 如果不存在，返回False，表示这是一个新的、不重复的题目
    return expression in existing_expressions

# 替换乘除法运算符
def replace_div_with_divide(expression):
    # 正则表达式用于匹配分数，如 5/6
    fraction_pattern = r'\b\d+/\d+\b'

    # 使用正则表达式找到所有的分数
    fractions = re.findall(fraction_pattern, expression)

    # 对于每个找到的分数，我们将其从原表达式中替换为一个占位符
    placeholders = []
    for i, fraction in enumerate(fractions):
        placeholder = f"{{fraction_{i}}}"
        placeholders.append(placeholder)
        expression = expression.replace(fraction, placeholder)

    # 将除法操作符 '/' 替换为 '÷'
    expression = expression.replace('/', '÷')
    # 将乘法操作符 '*' 替换为 'x'
    expression = expression.replace('*', '×')

    # 将占位符替换回原来的分数
    for i, placeholder in enumerate(placeholders):
        expression = expression.replace(placeholder, fractions[i])

    return expression

# 生成表达式文件
def creat_es(args):
    # 初始化两个集合，分别用于存储题目和答案
    # exercises = set()
    exercises = []
    answers = []
    # 循环直到生成指定数量的题目
    while len(exercises) < args.n:
        # 生成一个表达式
        expression = generate_expression(args.r, 3)
        # 检查表达式是否重复，如果不重复则添加到题目集合中
        if not is_duplicate(expression, exercises):
            # 计算表达式的答案，并添加到答案列表中
            answer = calculate_expression(expression)
            if (answer[0] != '-'):
                exercises.append(expression)
                answers.append(answer)
                #print(answer)

    # 使用列表推导式批量处理表达式
    processed_exercises = [replace_div_with_divide(expr) for expr in exercises]
    for expr in processed_exercises:
        print(expr)

    # 打开Exercises.txt和Answers.txt文件进行写入
    with open('Exercises.txt', 'w') as ef, open('Answers.txt', 'w') as af:
        # 遍历题目和答案，将它们写入相应的文件
        for i, (processed_exercise, answer) in enumerate(zip(processed_exercises, answers), 1):
            ef.write(f"{i}. {processed_exercise} =\n")
            af.write(f"{i}. {answer}\n")

# 评分
def grade(args):
    # 打开题目文件和答案文件进行读取
    with open(args.e, 'r') as ef, open(args.a, 'r') as af:
        # 读取题目和答案文件中的所有行
        exercises = ef.readlines()
        answers = af.readlines()
        # 初始化两个列表，分别用于存储正确和错误的题目编号
        correct = []
        wrong = []
        # 遍历题目和答案的每一对，并使用enumerate来跟踪编号
        for i, (exercise, answer) in enumerate(zip(exercises, answers), 1):
            # 去除题目和答案两端的空白字符
            exercise = exercise.strip()
            answer = answer.strip()
            # 如果计算出的题目结果等于答案文件中的答案，则标记为正确
            if calculate_expression(exercise.split('=')[0].strip()) == answer:
                correct.append(i)
            else:
                # 否则标记为错误
                wrong.append(i)
        # 打开Grade.txt文件进行写入
        with open('Grade.txt', 'w') as gf:
            # 写入正确题目的数量和编号
            gf.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
            # 写入错误题目的数量和编号
            gf.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})")

# 主程序
def main():
    parser = argparse.ArgumentParser(description='Generate arithmetic exercises.')
    # 添加参数'-n'，指定生成题目的数量，类型为整数
    parser.add_argument('-n', type=int, help='Number of exercises to generate')
    # 添加参数'-r'，指定题目中数值的最大范围，类型为整数，并且是必须提供的参数
    parser.add_argument('-r', type=int, required=True, help='Maximum value for numbers in exercises')
    # 添加参数'-e'，指定题目文件，类型为字符串
    parser.add_argument('-e', type=str, help='Exercise file')
    # 添加参数'-a'，指定答案文件，类型为字符串
    parser.add_argument('-a', type=str, help='Answer file')
    # 解析命令行参数
    args = parser.parse_args()

    # 如果提供了'-e'和'-a'参数，则进入评分模式
    if args.e and args.a:
        grade(args)
    else:
        # 如果没有提供'-e'和'-a'参数，则进入生成题目模式
        # 检查是否提供了必要的参数'-n'和'-r'
        if args.n is None or args.r is None:
            # 如果没有提供，打印帮助信息并返回
            parser.print_help()
            return
        #生成表达式文件
        creat_es(args)

if __name__ == "__main__":
    main()
