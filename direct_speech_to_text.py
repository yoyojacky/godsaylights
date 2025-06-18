import pyaudio
import vosk

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

try:
    while True:
        # 从麦克风读取音频数据
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            # 如果识别成功，输出结果
            res = recognizer.Result()
            print(res)
        else:
            # 输出中间识别结果
            print(recognizer.PartialResult())

except KeyboardInterrupt:
    print("\n识别结束。")

finally:
    # 停止和关闭音频流
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 输出最终识别结果
    print("最终识别结果:", recognizer.FinalResult())

