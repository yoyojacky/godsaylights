#  Lattepanda Sigma 上帝说要有光项目

## 使用方法简介

* 操作系统： Ubuntu 22.04.5 LTS
* 仓库文件结构:
.
├── arduino-cli  #arduino-cli 工具二进制文件 
├── direct_speech_to_text.py # 语音转文本测试代码
├── download_tools_and_models.sh # 工具和模型下载脚本
├── godsaylight_v2.py   #上帝说要有光主程序
├── install_packages.sh # 安装依赖包脚本程序
├── README.md        # 说明文档
├── requirements.txt  # virtualenv 环境下需要安装的python库
├── test_micphone.py  # 测试麦克风脚本
├── test_ollama_api.py # 测试本地Ollama API脚本
└── test_vosk.py      # 测试vosk功能脚本 

## 执行脚本前准备

* 1. 安装软件包依赖

```bash
./download_tools_and_models.sh 
./install_packages.sh 

```
下载好的软件包记得解压. 

* 2. 构建虚拟环境:

```bash
virtualenv -p python3 venv 
cd venv
source bin/activate 
```

* 3. 安装python库
```bash
pip install -r requirements.txt 
```

* 4. 根据视频介绍开始测试麦克风
* 5. 测试ollama 本地API
* 6. 测试vosk语音识别
* 7. 测试arduino-cli工具编译上传效果
```bash
arduino-cli config init 
```
然后编辑/home/你账户/.arduino/arduino.yaml文件:

```cpp
board_manager:
  additional_urls: ['https://downloads.arduino.cc/packages/package_staging_index.json']
```
* 8.更新和测试

```bash
arduino-cli core update-index 
arduino-cli core install arduino:avr
arduino-cli board list-all
arduino-cli sketch new blink
编辑以下blink.ino，然后上传 
arduino-cli compile -b arduino:avr:leonardo -p /dev/ttyACM0 --upload 
```

* 9.最终实验
```python
python godsaylight.py 
```
* 10. 如果喜欢就给个start 




