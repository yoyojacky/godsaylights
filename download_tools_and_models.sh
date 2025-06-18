#!/bin/bash
cd ~/
wget https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Linux_64bit.tar.gz
wget https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip

if [[ $? -eq 0 ]];
then 
	echo -e "\e[32;49m Download OK...\e[0m"
	echo -e "\e[32;49m Unzip the package and have fun\e[0m"
fi
