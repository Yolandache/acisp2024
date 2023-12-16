import os
import shutil
import json
import tempfile
from concurrent.futures import ThreadPoolExecutor
from glob import glob
from tqdm import tqdm
from collections import Counter

def get_file_list(path):
    return glob(os.path.join(path, "**/*.apk"), recursive=True)

def extract_dependencies(apk_file):
    apktool_command = 'apktool -q d -s -f {path_apk} -o {path_save_file}'
    temp_folder = 'temp_' + os.path.basename(apk_file)
    apktool_command = apktool_command.format(path_apk=apk_file, path_save_file=temp_folder)
    apk = {
        'file_path': apk_file,
        'dependencies': []  # 使用集合存储唯一依赖项
    }
    try:
        os.system(apktool_command + '\n')
    except Exception as e:
        return apk
    try:
        if os.path.exists(temp_folder):
            lib_folder = os.path.join(temp_folder, "lib")
            for root, dirs, files in os.walk(lib_folder):
                for file in files:
                    if file.endswith(".so"):
                        apk['dependencies'].append(file)  # 使用add()添加唯一项到集合中
            shutil.rmtree(temp_folder, ignore_errors=True)
        return apk
    except:
        return apk

def process_apk(apk_file):
    try:
        apk_data = extract_dependencies(apk_file)
        return apk_data
    except Exception as e:
        print("Error while processing:", apk_file)
        print(e)  # 打印异常信息
        return None

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def count_occurrences(lst):
    count_dict = Counter(lst)
    return count_dict

def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

if __name__ == '__main__':
    output_file = "normal_data_output.json"
    path = r"D:\fakeapp\apps"
    file_list = get_file_list(path)
    # 基于文件大小过滤APK文件
    file_list = [apk for apk in file_list if os.path.getsize(apk) >= 1024 * 1024]
    print(len(file_list))
    # 使用ThreadPoolExecutor并发处理APK，提高I/O性能
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = []
        # 使用tqdm创建进度条
        with tqdm(total=len(file_list), desc="Processing APKs") as pbar:
            for result in executor.map(process_apk, file_list):
                if result is not None:  # 过滤掉处理失败的APK
                    results.append(result)
                pbar.update()

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)


    # 从输出的JSON文件中读取数据
    data = read_json_file(output_file)

    # 过滤掉没有依赖项的条目
    so_data = [entry for entry in data if len(entry['dependencies']) != 0]

    # 准备包含依赖项集合的列表
    all_sets = [set(entry['dependencies']) for entry in so_data]

    # 比较所有APK的依赖项集合，并计算Jaccard相似度，确保每对APK只计算一次
    similarities = {}
    similar_pairs = []
    num_apks = len(all_sets)
    for i in range(num_apks):
        for j in range(i+1, num_apks):
            set1 = all_sets[i]
            set2 = all_sets[j]
            pair_key = f"{i}_{j}"
            similarity = jaccard_similarity(set1, set2)
            similarities[pair_key] = similarity
            similar_pairs.append({
                'apk1': so_data[i]['file_path'],
                'apk2': so_data[j]['file_path'],
                'similarity': similarity
            })

    # 输出相似度最高的前N对APK
    N = 10
    sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:N]

    output_similarities_file = "normal_data_similarity.json"
    print("Process completed. Results written to", output_similarities_file)

    print(f"相似度最高的前{N}对APK:")
    for pair_key, similarity in sorted_similarities:
        i, j = map(int, pair_key.split('_'))
        apk1 = so_data[i]['file_path']
        apk2 = so_data[j]['file_path']
        print(f"{apk1} and {apk2}：similarity = {similarity:.2f}")

        # 将相似度最高的前N对APK和相似度保存到JSON文件
    with open(output_similarities_file, 'w') as f:
        json.dump(similar_pairs, f, indent=4)
