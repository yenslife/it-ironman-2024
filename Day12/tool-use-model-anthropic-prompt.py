# 使用 openai 的 API 來生成文本
import openai
from dotenv import load_dotenv # 載入 dotenv 套件
import os
from rich import print

load_dotenv() # 載入環境變數

model_name = "gpt-4o-mini"

# 從環境變數中取得 API 金鑰，並且設定給 openai
openai.api_key = os.getenv("OPENAI_API_KEY") 

client = openai.OpenAI() # 建立 OpenAI 客戶端

def calculate_letter_count(input_string, target_character):
    # 計算 input_string 中 target_character 的數量
    return input_string.count(target_character)

def format_string(ai_response_string):
    while True:
        start_index = ai_response_string.find("<API>") # 找到 <API> 的開始位置，如果找不到會回傳 -1
        if start_index == -1:
            break
        end_index = ai_response_string.find("</API>", start_index) # 找到 </API> 的結束位置
        if end_index == -1:
            break
        api_content = ai_response_string[start_index+5:end_index] # 取得 API 內容
        input_string, target_character = api_content.split(',') # 分割 input_string 和 target_character
        letter_count = calculate_letter_count(input_string.strip(), target_character.strip()) # 計算字母數量
        ai_response_string = ai_response_string[:start_index] + str(letter_count) + ai_response_string[end_index+6:] # 把計算結果放回 ai_response_string 中
    return ai_response_string

# 提示的 propmt
prompt = '''
你是一個協助計算字母數量的AI助手。你的任務是回答使用者關於特定字串中某個字母出現次數的問題。

當需要計算字母數量時，你應該使用以下格式：
<API>input_string,target_character</API>

這個API標籤會自動計算input_string中target_character的出現次數。你應該將這個標籤直接插入到你的回答中，就像它是一個數字一樣。

回答時，請遵循以下指示：
1. 使用繁體中文回答。
2. 直接在需要顯示計算結果的地方使用<API>標籤。
3. 不要解釋計算過程，只需呈現結果。
4. 確保你的回答聽起來自然且合理。

例子：
問題：apple 中有幾個 p ？
回答： "apple" 中有<API>apple,p</API>個"p"。

問題：butterfly裡的t出現了幾次？
回答：在"butterfly" 這個單詞中，t出現了<API>butterfly,t</API>次。

注意事項：
- 不要在<API>標籤內使用引號。
- 在input_string和target_character之間不要加入任何符號（如逗號或空格）。
- 不要額外解釋<API>標籤的功能，直接將它視為計算結果使用。

現在，請回答以下問題：
<question>{$USER_QUESTION}</question>
'''

# 初始化對話歷史
messages = [
    {
        "role": "system",
        "content": prompt
    }
]

user_input = input("你：")

# 將用戶輸入加到對話歷史
messages.append({"role": "user", "content": user_input})

    
# 發送請求給 OpenAI API
completion = client.chat.completions.create(
    model=model_name,
    messages=messages
    )
    
# 獲取 AI 的回應
ai_response = completion.choices[0].message.content

print("\nLLM 原始輸出：")
print(ai_response)
print()

ai_response = format_string(ai_response)
    
# 印出 AI 的回應
print("格式化後的輸出")
print(f"AI：{ai_response}")

# test case: 請問 strawberry 這個字串中有幾個 r？banana 這個字串中有幾個 n？把這兩個字串串在一起，這樣會有幾個 a？