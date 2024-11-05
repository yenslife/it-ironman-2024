from groq import Groq
import json
from rich import print
client = Groq()
# MODEL = 'llama3-groq-70b-8192-tool-use-preview'
MODEL = 'llama3-groq-8b-8192-tool-use-preview'
# MODEL = 'llama3-8b-8192'

def calculate_letter_count(input_string, target_character):
    # 計算 input_string 中 target_character 的數量
    return str(input_string.count(target_character))

def run_conversation(user_prompt):
    messages=[
        {
            "role": "system",
            "content": "You are an assistant that can calculate how many times a specific letter appears in a string. Use the calculate_letter_count function to calculate the count."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate_letter_count",
                "description": "Calculate how many times a specific letter appears in a string",
                "parameters": {
                    "type": "object",
                    "properties": { 
                        "input_string": {
                            "type": "string",
                            "description": "The string to calculate the letter count of",
                        },
                        "target_character": {
                            "type": "string",
                            "description": "The letter to count in the input string",
                        }
                    },
                    "required": ["input_string", "target_character"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto", # auto: 自動選擇是否使用工具, required: 需要使用工具, none: 不使用工具
        max_tokens=4096
    )
    response_message = response.choices[0].message
    
    # 取得工具呼叫
    tool_calls = response_message.tool_calls
    # print(tool_calls)
    if tool_calls:
        available_functions = {
            "calculate_letter_count": calculate_letter_count,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                input_string=function_args.get("input_string"),
                target_character=function_args.get("target_character")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        # print(messages)
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content

# user_prompt = "What is 25 * 4 + 10?"
# user_prompt = "Say hi to me"
user_prompt = "How many times does the letter 'a' appear in the string 'banana'?xd"
# user_prompt = "How many times does the letter 'a' appear in the string 'banaaaaaaaaxxxxna'?"
# user_prompt = "你知道 srtrawberrrrrry 有多少個 r 嗎"
user_prompt = "你知道 strawberry 有多少個 r 嗎？笑死你最好會"
# user_prompt = "Do you know how many 'r's are in 'strawberry'? You better know, or I'll laugh to death!"
# user_prompt = user_prompt + "If you feel funny, append 'XD' to the end of your response"
print(run_conversation(user_prompt))