import json
import os

input_file_path = "D:/DDesktop/LLM_code/Knowledge/ANAH/anah/event.jsonl"
output_dir = "D:/DDesktop/LLM_code/Knowledge/data/anah/" 

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file_path, 'r', encoding='utf-8') as file:
    document_counter = 1
    for idx, line in enumerate(file):
        try:
            data = json.loads(line)
            
            if 'documents' in data:
                documents = data['documents']
                
                for doc in documents:
                    file_name = f"{str(document_counter).zfill(3)}.txt"
                    output_file_path = os.path.join(output_dir, file_name)
                    
                    with open(output_file_path, 'w', encoding='gbk') as output_file:
                        output_file.write(doc)
                    
                    print(f"Saved document {document_counter} as {file_name}")
                    document_counter += 1
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line {idx+1}: {e}")

print("Document extraction completed.")
