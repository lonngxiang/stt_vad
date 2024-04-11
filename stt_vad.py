import pyaudio
import wave
import time

import requests
import webrtcvad

CHUNK = 320  # 20ms 的语音帧
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
WAVE_OUTPUT_FILENAME = r"D:\**\output_realtime.wav"

vad = webrtcvad.Vad(3)  # 设置 VAD 的敏感度级别为 3

p = pyaudio.PyAudio()
stream = None

def get_record():
    global stream

    # 如果之前已经打开了音频流,先关闭它
    if stream is not None:
        stream.stop_stream()
        stream.close()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=0)

    print("start recording")
    frames = []
    last_active_time = time.time()

    while True:
        data = stream.read(CHUNK)
        if vad.is_speech(data, RATE):
            frames.append(data)
            last_active_time = time.time()
        else:
            if time.time() - last_active_time > 1.5: ##可以设置声音沉默时间，这里没人说话1.5秒停止退出
                break

    print("* 录音结束")
    print("frames 长度:",len(frames))



    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"已保存声音文件: {WAVE_OUTPUT_FILENAME}")
    print("stop recording")
    




while True:
	##1、声音录制
    get_record()
    # try:
    ##2 后续
    voice_input = get_asr(WAVE_OUTPUT_FILENAME)
    time.sleep(1)
    print("ni hao") 
    

