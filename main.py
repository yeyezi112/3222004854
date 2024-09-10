import os
import re
import jieba
import sys

#读取文件
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

#计算相似度
def calculate_similarity(original, original_add):
    #将文本用列表保存，并去掉其中标点符号
    original_clean = re.sub(r'[^\w\s]', '', original)
    original_clean = re.sub(r'\n', '', original_clean)
    original_add_clean = re.sub(r'[^\w\s]', '', original_add)

    # 使用jieba进行中文分词
    original_words = list(jieba.cut(original))
    original_add_words = list(jieba.cut(original_add))

    """
    print(original_words)
    print(original_add_words)
    """

    # 计算两个列表的交集
    common_words = [word for word in original_words if word in original_add_words]

    #print(common_words)

    # 计算相似度
    similarity = (2 * len(common_words)) / (len(original_words) + len(original_add_words))
    return similarity

#输出结果
def write_result(result_file, similarity):
    with open(result_file, 'w', encoding='utf-8') as file:
        file.write(f"{similarity * 100:.0f}%")

#main函数
def main():
    #读取文件
    if len(sys.argv) != 4:
        for arg in sys.argv:
            print(arg)
        print("Usage: python script.py <path_to_original> <path_to_original_add> <path_to_result>")
        sys.exit(1)

    original_path = sys.argv[1]
    original_add_path = sys.argv[2]
    result_path = sys.argv[3]

    if not os.path.isfile(original_path) or not os.path.isfile(original_add_path):
        print("Error: One of the provided file paths does not exist.")
        sys.exit(1)

    original_text = read_file(original_path)
    original_add_text = read_file(original_add_path)

    #计算相似度并输出
    similarity = calculate_similarity(original_text, original_add_text)
    print(f"{similarity * 100:.0f}%")
    write_result(result_path, similarity)


if __name__ == "__main__":
    main()
