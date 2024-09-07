import os
import sys

#读取文件
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

#计算相似度
def calculate_similarity(original, original_add):
    # 将文本分词，这里简单地以单个汉字为单位
    original_words = set(original.replace(' ', ''))
    original_add_words = set(original_add.replace(' ', ''))

    # 计算两个集合的交集
    common_words = original_words.intersection(original_add_words)

    # 计算相似度
    similarity = (2 * len(common_words)) / (len(original_words) + len(original_add_words))
    return similarity

#输出结果
def write_result(result_file, similarity):
    with open(result_file, 'w', encoding='utf-8') as file:
        file.write(f"{similarity * 100:.0f}%")

#main函数
def main():
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

    similarity = calculate_similarity(original_text, original_add_text)
    print(f"{similarity * 100:.0f}%")
    write_result(result_path, similarity)


if __name__ == "__main__":
    main()
