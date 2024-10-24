import json
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

# 1. 加载 train.json 和 test.json
with open('/home/rqn/ANAH/anah/train.json', 'r', encoding='utf-8') as f:
    train_data = json.load(f)

with open('/home/rqn/ANAH/anah/test.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

# 2. 加载模型和 tokenizer
model_name = "/home/rqn/xtuner/Shanghai_AI_Laboratory/internlm2-chat-7b"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name, trust_remote_code=True)

# 3. 定义生成 embeddings 的函数
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
        hidden_states = outputs.hidden_states[-1]  # 获取最后一层的隐藏状态
    return hidden_states.mean(dim=1).squeeze().cpu().numpy()

# 4. 为 train 和 test 数据生成 embeddings
print("正在为训练数据生成 embeddings...")
train_embeddings = {}
for key, value in train_data.items():
    train_embeddings[key] = get_embedding(value)

print("正在为测试数据生成 embeddings...")
test_embeddings = {}
for key, value in test_data.items():
    test_embeddings[key] = get_embedding(value)

# 5. 对每个 test 数据计算与 train 数据的相似度并找到最相似的 3 个
matched_data = []
for test_key, test_emb in test_embeddings.items():
    similarities = {}
    for train_key, train_emb in train_embeddings.items():
        # 计算余弦相似度
        similarity = cosine_similarity([test_emb], [train_emb])[0][0]
        similarities[train_key] = similarity

    # 找到最相似的 3 个 train 数据
    top_3 = sorted(similarities.items(), key=lambda item: item[1], reverse=True)[:3]

    # 将 top 3 的 train_key 和 train_value 添加到 matched_data 列表中
    for train_key, _ in top_3:
        matched_data.append({
            "train_key": train_key,
            "train_value": train_data[train_key]
        })

# 6. 去重 matched_data 列表
# 使用 train_key 进行去重
unique_matched_data = {item['train_key']: item for item in matched_data}
unique_matched_data = list(unique_matched_data.values())

# 7. 保存结果为 embadding_sample.json
with open('/home/rqn/ANAH/anah/embadding_sample.json', 'w', encoding='utf-8') as f:
    json.dump(unique_matched_data, f, ensure_ascii=False, indent=4)

print("聚类完成，结果已保存为 embadding_sample.json")
