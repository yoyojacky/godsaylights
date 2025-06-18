import pyaudio
import vosk
import requests
import json
import os
import subprocess

# 设置 Vosk 模型路径
model_path = './vosk-model-small-cn-0.22'  # 如果使用中文模型，替换为你的模型路径

# 初始化 Vosk 模型和识别器
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)  # 假设麦克风的音频采样率是 16000Hz

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 打开麦克风音频流
stream = p.open(
    format=pyaudio.paInt16,  # 音频格式
    channels=1,              # 单声道
    rate=16000,              # 采样率，需与模型采样率一致
    input=True,              # 表示是录音
    frames_per_buffer=8000   # 缓冲区大小
)

print("开始说话，按 Ctrl+C 停止...")

# 检查保存目录是否存在，不存在则创建
blink_dir = "./blink"
if not os.path.exists(blink_dir):
    os.makedirs(blink_dir)

OLLAMA_API_URL = "http://127.0.0.1:11434"  # 请确保 Ollama 服务已启动并监听此地址

#model_name = "llama3.1:8b"  # 根据你的模型名称调整
model_name = "gemma3:4b"  # 根据你的模型名称调整
max_tokens = 150


def process_api_response(response):
    try:
        if response.status_code == 200:
            full_text = ""
            # 逐行读取并解析响应内容
            for line in response.iter_lines():
                if line:
                    line_data = line.decode("utf-8")
                    try:
                        json_data = json.loads(line_data)
                        if "content" in json_data.get("message", {}):
                            content = json_data["message"]["content"]
                            content = content.replace("cpp", "").replace("c","").replace("arduino","").replace("c++", "").replace("```", "").replace("cpp","")
                            full_text += content
                    except json.JSONDecodeError:
                        print(f"无法解析 JSON 数据: {line_data}")
            return full_text
        else:
            print(f"API 请求失败: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求处理失败: {e}")
        return None

try:
    while True:
        # 从麦克风读取音频数据
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            # 如果识别成功，输出结果
            res = recognizer.Result()
            #print(res)
            
            # 解析识别结果
            try:
                result_json = json.loads(res)
                if 'text' in result_json:
                    recognized_text = result_json['text'].strip(' ')
                    print(f"识别到的内容: {recognized_text}")
                    
                    # 判断是否包含特定关键词
                    if "上帝" in recognized_text:
                        print("检测到语音指令: 上帝说要有光")
                        
                        # 生成高电平模式的代码
                        prompt = '请只输出Arduino代码，使用GPIO7引脚, 引脚模式设置为输出,并在loop()函数中设置为高电平，不添加任何解释或总结,也不要添加任何格式化代码。'
                        response = requests.post(
                            f"{OLLAMA_API_URL}/api/chat",
                            json={
                                "model": model_name,
                                "messages": [
                                    {"role": "user", "content": prompt}
                                ],
                                "max_tokens": max_tokens
                            },
                            timeout=10  # 设置超时时间为 10 秒
                        )
                        
                        full_text = process_api_response(response)
                        if full_text:
                            print("生成的代码:")
                            print(full_text)
                            
                            # 保存代码到文件
                            with open(os.path.join(blink_dir, "blink.ino"), "w") as f:
                                f.write(full_text)
                            print("代码已保存到 blink/blink.ino")
                            
                            # 切换到 blink 目录并执行编译上传命令
                            os.chdir(blink_dir)
                            compile_upload_cmd = "sudo arduino-cli compile -b arduino:avr:leonardo -p /dev/ttyACM0 --upload"
                            print(f"执行命令: {compile_upload_cmd}")
                            subprocess.run(compile_upload_cmd, shell=True)
                            os.chdir("..")  # 返回原目录
                            
                    elif "天黑" in recognized_text:
                        print("检测到语音指令: 天黑请闭眼")
                        
                        # 生成低电平模式的代码
                        prompt = '请只输出完整的Arduino代码，内容是设置变量LED为GPIO7, 在setup()函数中该引脚设置为输出，并在loop()循环中输出LED为低电平，不添加任何解释或总结,不要添加"```cpp"或者"```c"，或者"```arduino"，"```c++"等等格式化代码。'
                        response = requests.post(
                            f"{OLLAMA_API_URL}/api/chat",
                            json={
                                "model": model_name,
                                "messages": [
                                    {"role": "user", "content": prompt}
                                ],
                                "max_tokens": max_tokens
                            },
                            timeout=10  # 设置超时时间为 10 秒
                        )
                        
                        full_text = process_api_response(response)
                        if full_text:
                            print("生成的代码:")
                            print(full_text)
                            
                            # 保存代码到文件
                            with open(os.path.join(blink_dir, "blink.ino"), "w") as f:
                                f.write(full_text)
                            print("代码已保存到 blink/blink.ino")
                            
                            # 切换到 blink 目录并执行编译上传命令
                            os.chdir(blink_dir)
                            compile_upload_cmd = "sudo arduino-cli compile -b arduino:avr:leonardo -p /dev/ttyACM0 --upload"
                            print(f"执行命令: {compile_upload_cmd}")
                            subprocess.run(compile_upload_cmd, shell=True)
                            os.chdir("..")  # 返回原目录
                            
            except json.JSONDecodeError:
                print("无法解析语音识别结果")
        else:
            # 获取中间识别结果
            partial_res = recognizer.PartialResult()
            # 移除引号并检查是否为空
            partial_res = partial_res.strip('"')
            if partial_res:
                # 输出非空的中间识别结果
                #print(f"中间识别结果: {partial_res}")
                pass

except KeyboardInterrupt:
    print("\n识别结束。")

finally:
    # 停止和关闭音频流
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # 输出最终识别结果
    print("最终识别结果:", recognizer.FinalResult())
