import wave 
import vosk


model_path = "vosk-model-chs-0.68"

model = vosk.Model(model_path)

rec = vosk.KaldiRecognizer(model, 44100)

wf = wave.open("output.wav", 'rb')


while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        print(result) 

result = rec.FinalResult()
print(result)
