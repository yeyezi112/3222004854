import subprocess
import unittest

from main import calculate_similarity

class MyTestCase(unittest.TestCase):
    #普通情况
    def test_common(self):
        self.assertGreater(calculate_similarity('他是一个聪明的人，总能迅速解决问题。',
                                                '她是一个聪明的人，总能迅速解决问题。'), 0.9)

    #专业术语
    def test_profession(self):
        self.assertGreater(calculate_similarity('随着全球气候变化的加剧，我们必须采取行动来减少温室气体排放，并寻找可持续的能源解决方案。',
                                                '面对全球气候变暖的挑战，我们迫切需要采取措施减少温室气体排放，并探索可再生的能源选择。'),
                           0.5)
    def test_lowsimilarity(self):
        self.assertGreater(calculate_similarity('Python是一种高级编程语言，它的设计哲学是“优雅”、“明确”、“简单”。Python拥有动态类型系统和垃圾回收功能，能够自动管理内存使用，并且支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。'
                                                'Python的语法简洁而清晰，使用缩进来表示代码块，从而减少了代码的冗余。Python解释器本身几乎可以在所有的操作系统中运行。Python的标准库提供了丰富的功能，包括图形界面、数据库、网络、多线程、正则表达式等。'
                                                'Python还有许多第三方库和框架，可以用于科学计算、数据分析、机器学习、Web开发等领域。Python是一种通用的编程语言，适用于各种应用场景。',
                                                'Python是一门通用的高级编程语言。它具有简单明确的语法，'
                                                '使用缩进来组织代码结构。Python支持多种编程范式，如面向对象、函数式和过程式编程。Python具有动态类型系统和自动内存管理功能，可以适应不同的需求和环境。Python可以在多种操作系统中运行，并且拥有庞大的标准库和第三方库，'
                                                '涵盖了图形界面、数据库、网络、多线程、正则表达式等各种功能。Python还可以用于科学计算、数据分析、机器学习、Web开发等领域。Python是一门优雅而强大的编程语言，适合各种应用场景。')
                           , 0.4)

    #长文本
    def test_long(self):
        self.assertGreater(calculate_similarity('近年来，全球气候变化已经成为人类面临的一个重大挑战。气候变化不仅导致极端天气事件的增加，'
                                                '还可能导致海平面上升、生态系统破坏和生物多样性丧失等问题。为了应对气候变化，各国政府'
                                                '和国际组织已经采取了一系列的措施。例如，制定和实施气候变化应对政策，推动可再生能源的发展'
                                                '和利用，以及提高公众对气候变化的认识和参与。然而，要实现全球气候变化的有效控制，还需要'
                                                '全球范围内的合作和共同努力。', '近年来，全球气候变暖已经成为人类面临的'
                                            '一个重大挑战。气候变化不仅导致极端天气事件的增加，还可能导致海平面上升、生态系统破坏和'
                                     '生物多样性丧失等问题。为了应对气候变化，各国政府和国际组织已经采取了一系列的措施。例如，'
                                       '制定和实施气候变化应对政策，推动可再生能源的发展和利用，以及提高公众对气候变化的认识和参与。'
                                        '然而，要实现全球气候变暖的有效控制，还需要全球范围内的合作和共同努力。'), 0.8)

    #英语
    def test_English(self):
        self.assertGreater(calculate_similarity('I love studying Computer Science.',
                                                'I enjoy studying Computer Science.'), 0.8)

    #中英混杂
    def test_Chiglish(self):
        self.assertGreater(calculate_similarity('我喜欢学习Computer Science。',
                                                '我很高兴能学会Computer Science。'), 0.6)

    #调整语序
    def test_order(self):
        self.assertGreater(calculate_similarity('我已经学习和练习Linux。', '我已经练习和学习Linux。'), 0.7)

    #空白输入
    def test_empty(self):
        self.assertEqual(calculate_similarity('我很好。', ''), 0)

    #文件路径错误
    def test_nullfile(self):
        result = subprocess.run(
            ['python', 'D:\大三上\Homework\main.py', '--param1', 'D:\大三上\\ruangong_test\original.txt',
             '--param2','D:\大三上\\ruangong_test\original_add1.txt',
             '--param3', 'D:\大三上\\ruangong_test\similarity.txt'
             ], stdout=subprocess.PIPE)
        stdout = result.stdout.decode
        print(stdout)

    #缺少文件路径
    def test_lackfile(self):
        result = subprocess.run(
            ['python', 'D:\大三上\Homework\main.py', '--param1', 'D:\大三上\\ruangong_test\original.txt',
             '--param2',
             '--param3', 'D:\大三上\\ruangong_test\similarity.txt'
             ], stdout=subprocess.PIPE)
        stdout = result.stdout.decode
        print(stdout)

if __name__ == '__main__':
    unittest.main()
