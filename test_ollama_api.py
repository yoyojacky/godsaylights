import requests
import json

OLLAMA_API_URL = "http://127.0.0.1:11434"

model_name = "llama3.1:8b"  # 根据你的模型名称调整
prompt = 'please show me a blink led by using GPIO7 on arduino, just output demo code,do not explain, do not summarize, just output the demo code.'
max_tokens = 150

try:
    response = requests.post(
        f"{OLLAMA_API_URL}/api/chat",
        json={
            "model": model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens
        },
        stream=True,  # 使用流式传输
        timeout=10  # 设置超时时间为 10 秒
    )

    # 检查响应是否成功
    if response.status_code == 200:
        full_text = ""  # 用于存储完整的文本结果
        for line in response.iter_lines():
            if line:
                try:
                    # 尝试解码每一行
                    line_data = line.decode("utf-8")
                    # 尝试解析 JSON 数据
                    json_data = json.loads(line_data)
                    # 检查是否包含 'content' 字段
                    if "content" in json_data.get("message", {}):
                        full_text += json_data["message"]["content"]
                except (UnicodeDecodeError, json.JSONDecodeError):
                    pass  # 如果解码或解析失败，跳过这一行
        print(full_text)
    else:
        print(f"Error: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
