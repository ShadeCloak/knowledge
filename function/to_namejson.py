"""
import json
import os

# 定义要处理的文件路径列表，添加绝对路径
jsonl_files = [
    '/home/rqn/ANAH/anah/thing.jsonl',
    '/home/rqn/ANAH/anah/event.jsonl',
    '/home/rqn/ANAH/anah/location.jsonl',
    '/home/rqn/ANAH/anah/person.jsonl'
]

# 存储提取出来的结果
output = {}

# 序号初始化
index = 1

# 遍历每个 JSONL 文件
for file in jsonl_files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            try:
                # 逐行读取每个 JSON 对象
                for line in f:
                    try:
                        # 加载每一行的 JSON 对象
                        item = json.loads(line.strip())
                        # 检查是否有 'name' 字段
                        if 'name' in item:
                            # 添加到输出字典，带上序号
                            output[index] = item['name']
                            index += 1
                        else:
                            print(f"警告: 文件 {file} 中的某项没有 'name' 字段: {item}")
                    except json.JSONDecodeError as e:
                        print(f"文件 {file} 中的一行解析错误: {e}")
            except Exception as e:
                print(f"处理文件 {file} 时出错: {e}")
    else:
        print(f"错误: 找不到文件 {file}")

# 如果有内容则保存到文件
if output:
    output_file = '/home/rqn/ANAH/anah/name.json'  # 新的输出文件路径
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)


import json
import random

# 读取原始的 name.json 文件
input_file = '/home/rqn/ANAH/anah/name.json'
train_output_file = '/home/rqn/ANAH/anah/train.json'
test_output_file = '/home/rqn/ANAH/anah/test.json'

# 超参数：测试集的比例
test_ratio = 0.2

# 打开并读取 name.json 文件
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取所有的项并打乱顺序
all_items = list(data.items())  # 转换为 (key, value) 的列表
random.shuffle(all_items)  # 打乱列表顺序

# 计算测试集的大小
test_size = int(len(all_items) * test_ratio)

# 划分为测试集和训练集
test_set = all_items[:test_size]
train_set = all_items[test_size:]

# 转换为字典格式
train_dict = {k: v for k, v in train_set}
test_dict = {k: v for k, v in test_set}

# 将训练集写入 train.json
with open(train_output_file, 'w', encoding='utf-8') as f:
    json.dump(train_dict, f, ensure_ascii=False, indent=4)

# 将测试集写入 test.json
with open(test_output_file, 'w', encoding='utf-8') as f:
    json.dump(test_dict, f, ensure_ascii=False, indent=4)

print(f"训练集已保存到 {train_output_file}")
print(f"测试集已保存到 {test_output_file}")
"""
import json
import random

# 输入文件路径：之前生成的 train.json 文件
train_input_file = '/home/rqn/ANAH/anah/train.json'
sample_output_file = '/home/rqn/ANAH/anah/random_sample.json'

# 超参数：采样比例
sample_ratio = 0.4  # 比如默认采样30%

# 打开并读取 train.json 文件
with open(train_input_file, 'r', encoding='utf-8') as f:
    train_data = json.load(f)

# 获取所有的项并打乱顺序
train_items = list(train_data.items())  # 转换为 (key, value) 的列表
random.shuffle(train_items)  # 打乱顺序以确保随机采样

# 计算采样集的大小
sample_size = int(len(train_items) * sample_ratio)

# 从打乱的训练集里采样
sample_set = train_items[:sample_size]

# 转换为字典格式
sample_dict = {k: v for k, v in sample_set}

# 将采样后的数据保存为 sample.json
with open(sample_output_file, 'w', encoding='utf-8') as f:
    json.dump(sample_dict, f, ensure_ascii=False, indent=4)

print(f"随机采样数据已保存到 {sample_output_file}")
