import json

def convert_to_training_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)

            # 构造训练数据格式
            for i in range(len(data["selected_questions"])):
                # 用户问题
                prompt = {"content": data["selected_questions"][i], "role": "user"}

                # 模型回答处理（假设选择 InternLM 作为 chosen，GPT3.5 作为 rejected）
                if isinstance(data["GPT3.5_answers_D"][i], list):
                    chosen_content = " ".join(data["GPT3.5_answers_D"][i])
                else:
                    chosen_content = data["GPT3.5_answers_D"][i]

                if isinstance(data["InternLM_answers"][i], list):
                    rejected_content = " ".join(data["InternLM_answers"][i])
                else:
                    rejected_content = data["InternLM_answers"][i]

                # 只有当 chosen 和 rejected 都有内容时，才生成新的 JSON 格式
                if chosen_content and chosen_content.strip() and rejected_content and rejected_content.strip():
                    new_data = {
                        "prompt": [prompt],
                        "chosen": [{"content": chosen_content, "role": "assistant"}],
                        "rejected": [{"content": rejected_content, "role": "assistant"}]
                    }
                    # 将结果写入新文件中
                    outfile.write(json.dumps(new_data, ensure_ascii=False) + '\n')

# 调用函数，进行格式转换
convert_to_training_format('/home/rqn/ANAH/anah/random_sample.jsonl', '/home/rqn/ANAH/anah/training_sample2.jsonl')
