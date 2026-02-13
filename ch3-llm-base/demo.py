import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 指定模型id 设备
model_id = "Qwen/Qwen1.5-0.5B-Chat"
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# 加载模型和分词器
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_id)
print("模型和分词器加载完成！")

# 准备对话输入
messages = [
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "你好，请介绍你自己."}
]

# 使用分词器模板格式化输入
text = tokenizer.apply_chat_template(
  messages,
  tokenize=False,
  add_generation_prompt=True
)
# 用分词器把输入编码为向量
model_inputs = tokenizer([text], return_tensor="pt").to(device)
print("编码后的输入文本：")
print(model_inputs)

# 使用模型生成回答
input_ids_tensor = torch.tensor(model_inputs["input_ids"]).to(device) # 转换成tensor
generated_ids = model.generate(
  input_ids=input_ids_tensor,
  max_new_tokens=512 # 模型最多能生成多少新的token
)
# 截取生成的token id中的输入部分，只留下模型新生成的部分
generated_ids = [
  output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

# 解码生成的token id
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print("\n模型的回答：")
print(response)


