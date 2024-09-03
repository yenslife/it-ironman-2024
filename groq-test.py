# 檔名為 groq-test.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

input_string = "你好ㄚ可愛的模型"
model_name = "llama3-8b-8192"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": input_string,
        }
    ],
    model=model_name,
)

print(chat_completion.choices[0].message.content)