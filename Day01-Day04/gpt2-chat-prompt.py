from transformers import GPT2LMHeadModel, GPT2Tokenizer

# 載入預訓練的 GPT-2 模型和分詞器
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)    # 載入模型
tokenizer = GPT2Tokenizer.from_pretrained(model_name)  # 載入分詞器

# 設定輸入的字串
input_string = "User: What is AI?\nAssistant:"

# 將字串編碼為模型可以接受的格式，也就是 token
input_ids = tokenizer.encode(input_string, return_tensors='pt')

# 生成後續文本
output = model.generate(
    input_ids,              # 輸入的 token
    max_length=50,         # 生成文本的最大長度
    num_return_sequences=1, # 生成幾個句子
    no_repeat_ngram_size=2, # 避免重複的 n-gram
)

# 解碼生成的 id 為字串
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

# 打印原始輸出
print("output:")
print(generated_text)