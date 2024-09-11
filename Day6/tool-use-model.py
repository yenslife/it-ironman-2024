# 使用 openai 的 API 來生成文本
import openai
from dotenv import load_dotenv # 載入 dotenv 套件
import os

load_dotenv() # 載入環境變數

model_name = "gpt-4o-mini"

# 從環境變數中取得 API 金鑰，並且設定給 openai
openai.api_key = os.getenv("OPENAI_API_KEY") 

client = openai.OpenAI() # 建立 OpenAI 客戶端

def calculate_letter_count(input_string, target_character):
    # 計算 input_string 中 target_character 的數量
    return input_string.count(target_character)

def format_string(ai_response_string):
    start_index = ai_response_string.find("<API>") # 找到 <API> 的開始位置，如果找不到會回傳 -1
    if start_index != -1:
        end_index = ai_response_string.find("</API>", start_index) # 找到 </API> 的結束位置
        api_content = ai_response_string[start_index+5:end_index] # 取得 API 內容
        input_string, target_character = api_content.split(',') # 分割 input_string 和 target_character
        letter_count = calculate_letter_count(input_string.strip(), target_character.strip()) # 計算字母數量
        return ai_response_string[:start_index] + str(letter_count) + ai_response_string[end_index+6:] # 把計算結果放回 ai_response_string 中
    return ai_response_string

# 提示的 propmt
prompt = '''
你的任務是幫助使用者計算字母的數量。
在你要表達數字的地方用 <API>input_string, target_character</API> 來表達。
把 input_string 改成要計算的字串，target_character 改成目標字母。
注意：
1. 不要用引號來包住 input_string 和 target_character。
2. 不要在 input_string 和 target_character 之間加任何符號，例如逗號、空格或其他符號。
3. 不用額外說明計算過程，可以加上自然語言潤飾句子
4. 使用**繁體中文**回答問題。
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

ai_response = format_string(ai_response)
    
# 印出 AI 的回應
print(f"AI：{ai_response}")