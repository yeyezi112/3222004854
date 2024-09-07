def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def calculate_similarity(original, original_add):
    # 将文本分词，这里简单地以单个汉字为单位
    original_words = set(original.replace(' ', ''))
    original_add_words = set(original_add.replace(' ', ''))

    # 计算两个集合的交集
    common_words = original_words.intersection(original_add_words)

    # 计算相似度
    similarity = (2 * len(common_words)) / (len(original_words) + len(original_add_words))
    return similarity

def write_result(result_file, similarity):
    with open(result_file, 'w', encoding='utf-8') as file:
        file.write(f"{similarity:.2f}")
