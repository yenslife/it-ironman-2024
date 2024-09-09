import tiktoken

def calculate_token_count(input_string: str, model_name: str) -> int:
    
    # 使用 tiktoken 建立編碼器
    encoding = tiktoken.encoding_for_model(model_name)
    
    # 計算並印出 token 數量
    print(f"實際上的 token 組成：{encoding.encode(input_string)}")
    token_count = len(encoding.encode(input_string))
    print(f"token 數量：{token_count}")
    return token_count

if __name__ == "__main__":
    model_name = "gpt-4o-mini" 
    sample_input = "你好啊"
    token_count = calculate_token_count(sample_input, model_name)
    sample_input = "Hello my friend"
    token_count = calculate_token_count(sample_input, model_name)