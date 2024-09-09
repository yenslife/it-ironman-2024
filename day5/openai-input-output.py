# 檔名為 openai-test.py
# 使用 openai 的 API 來生成文本
import openai
from dotenv import load_dotenv # 載入 dotenv 套件
import os

load_dotenv() # 載入環境變數

model_name = "gpt-4o-mini"

# 從環境變數中取得 API 金鑰，並且設定給 openai
openai.api_key = os.getenv("OPENAI_API_KEY") 

client = openai.OpenAI() # 建立 OpenAI 客戶端

while True:

    # 獲取使用者輸入
    user_input = input("你：")

    messages = [
        {
            "role": "system",
            "content": "使用繁體中文回答問題"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    # 發送請求給 OpenAI API
    completion = client.chat.completions.create(
        model=model_name,
        messages=messages
    )
    
    # 獲取 AI 的回應
    ai_response = completion.choices[0].message.content
    
    # 印出 AI 的回應
    print(f"AI：{ai_response}")