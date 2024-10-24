import json

# 1. 加载 sample.json
sample_file = '/home/rqn/ANAH/anah/random_sample.json'
with open(sample_file, 'r', encoding='utf-8') as f:
    sample_data = json.load(f)

# 2. 加载所有 jsonl 文件
jsonl_files = [
    '/home/rqn/ANAH/anah/thing.jsonl',
    '/home/rqn/ANAH/anah/event.jsonl',
    '/home/rqn/ANAH/anah/location.jsonl',
    '/home/rqn/ANAH/anah/person.jsonl'
]

# 3. 将所有 jsonl 文件内容加载到一个列表中
all_entries = []
for jsonl_file in jsonl_files:
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            all_entries.append(json.loads(line))

# 4. 通过 sample.json 中的 name 标签筛选对应的项
selected_entries = []
sample_names = set(sample_data.values())  # 获取 sample.json 里面的 name 标签
for entry in all_entries:
    if entry["name"] in sample_names:
        selected_entries.append(entry)

# 5. 将筛选后的数据保存为新的 sample.jsonl 文件
output_file = '/home/rqn/ANAH/anah/random_sample.jsonl'
with open(output_file, 'w', encoding='utf-8') as f:
    for entry in selected_entries:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

print(f"已完成筛选，结果保存为 {output_file}")
