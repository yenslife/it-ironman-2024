from groq import Groq
import json
# from rich import print

client = Groq()
MODEL = 'llama3-groq-70b-8192-tool-use-preview'

def calculate(expression):
    """Evaluate a mathematical expression"""
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})

def run_conversation(user_prompt):
    messages=[
        {
            "role": "system",
            "content": "You are a calculator assistant. Use the calculate function to perform mathematical operations and provide the results."
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
                "name": "calculate",
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    # print(f"response: {response}")
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    print(f"response_message: {response_message}")
    print(f"tool_calls: {tool_calls}")
    if tool_calls:
        print(f"tool_calls: {tool_calls}")
        available_functions = {
            "calculate": calculate,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                expression=function_args.get("expression")
            )
            print(f"function_response: {function_response}")
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        print(f"messages: {messages}")
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content

user_prompt = "What is 25 * 4 + 10?"
# user_prompt = "Say hi to me"
print(run_conversation(user_prompt))