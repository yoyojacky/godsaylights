import alsaaudio


# list all audio input devices 
input_devices = alsaaudio.pcms(alsaaudio.PCM_CAPTURE)

print("Available device:") 
for device in input_devices:
    print(device)
