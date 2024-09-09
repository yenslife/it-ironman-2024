import openai
from dotenv import load_dotenv
import os
import tiktoken
import sys

load_dotenv() # 載入環境變數

model_name = "gpt-4o-mini"

# 從環境變數中取得 API 金鑰，並且設定給 openai
openai.api_key = os.getenv("OPENAI_API_KEY") 

client = openai.OpenAI() # 建立 OpenAI 客戶端

# 使用 tiktoken 建立編碼器
encoding = tiktoken.encoding_for_model(model_name)

# 初始化對話歷史
messages = [
    {
        "role": "system",
        "content": "使用繁體中文回答問題"
    }
]

while True:
    
    # 獲取用戶輸入
    user_input = input("你：")
    
    # 將用戶輸入加到對話歷史
    messages.append({"role": "user", "content": user_input})

    # 如果用戶輸入 '再見'，結束對話
    if user_input.lower() == '再見':
        print("AI：再見！很高興與你交談。")
        break
    
    # 計算當前對話紀錄的 token 數量
    total_tokens = sum(len(encoding.encode(msg["content"])) for msg in messages)
    print(f"目前 token 數量：{total_tokens}")

    # 當 token 超過 1000 時，移除最早的消息
    while total_tokens > 100:
        messages.pop(1)  # 移除最早的用戶或 AI 回應
        total_tokens = sum(len(encoding.encode(msg["content"])) for msg in messages)

    # 發送請求給 OpenAI API，使用 stream=True
    print("AI：", end="", flush=True)
    for chunk in client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True
    ):
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
            sys.stdout.flush()
    
    print()  # 換行
    
    # 獲取完整的 AI 回應
    ai_response = "".join(chunk.choices[0].delta.content or "" for chunk in client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True
    ))
    
    # 將 AI 的回應添加到對話歷史
    messages.append({"role": "assistant", "content": ai_response})