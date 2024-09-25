import random
import fractions
import argparse


# 生成随机数
def generate_number(max_value):
    if random.random() < 0.4:  # 40% 的概率生成真分数
        numerator = random.randint(1, max_value - 1)
        denominator = random.randint(numerator + 1, max_value)
        return fractions.Fraction(numerator, denominator)
    else:  # 60% 的概率生成自然数
        return random.randint(1, max_value)

# 生成四则运算表达式
def generate_expression(max_value, max_operators):
    # 定义一个列表，包含四则运算符。
    operators = ['+', '-', '×', '÷']
    # 初始化一个空字符串，用于构建算术表达式。
    expression = ""
    # 随机选择一个运算符的数量，这个数量不会超过max_operators。
    num_operators = random.randint(2, max_operators)

    # 循环num_operators次，每次循环都向表达式中添加一个运算符和一个数值（整数或分数）。
    for i in range(num_operators):
        # 如果不是第一个运算符，在运算符前添加一个空格。
        if i > 0:
            expression += " " + random.choice(operators) + " "
        expression += str(generate_number(max_value))

    # 返回构建好的算术表达式。
    return expression

# 计算表达式的值
def calculate_expression(expression):
    try:
        # 使用eval函数计算表达式的值
        result = eval(expression.replace('÷', '/').replace('×', '*'))

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

# 生成表达式文件
def creat_es(args):
    # 初始化两个集合，分别用于存储题目和答案
    exercises = []
    answers = []
    # 循环直到生成指定数量的题目
    while len(exercises) < args.n:
        # 生成一个表达式
        expression = generate_expression(args.r, 3)
        if expression not in exercises:
            # 计算表达式的答案，并添加到答案列表中
            answer = calculate_expression(expression)
            if (answer[0] != '-'):
                exercises.append(expression)
                answers.append(answer)
                #print(answer)

    # 打开Exercises.txt和Answers.txt文件进行写入
    with open('Exercises.txt', 'w') as ef, open('Answers.txt', 'w') as af:
        # 遍历题目和答案，将它们写入相应的文件
        for i, (exercise, answer) in enumerate(zip(exercises, answers), 1):
            ef.write(f"{i}. {exercise} =\n")
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
            # 去除题目和答案的编号
            exercise = exercise.split(".", 1)
            exercise = exercise[1].strip()
            # 去除题目的‘=’号
            exercise = exercise.split('=')[0].strip()
            answer = answer.split(".", 1)
            answer = answer[1].strip()
            # 如果计算出的题目结果等于答案文件中的答案，则标记为正确
            if calculate_expression(exercise) == answer:
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
    parser.add_argument('-r', type=int, help='Maximum value for numbers in exercises')
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
