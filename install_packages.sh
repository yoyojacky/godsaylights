#!/bin/bash
# 


sudo apt update && sudo apt upgrade -y 

if [[ $? -eq 0 ]];
then 
   for i in virtualenv build-essential gcc-12-i686-linux-gnu python3-dev libasound2-dev alsa-utils tree libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev net-tools openssh-server htop 
   do
	echo -e "\e[32:40mInstalling $i ...\e[0m"
        sudo apt -y install  $i
	if [[ $? -eq 0 ]];
	then
	  echo -e "\e[32:40mInstalling $i [OK].\e[0m"
	else 
	  echo -e "\e[34:40mInstalling $i [Failed].\e[0m"
        fi	  
    done 
fi

sudo apt autoremove -y
echo "Job done!"
