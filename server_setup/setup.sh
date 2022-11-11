#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if (( $EUID != 0 )); then
	printf "${RED}[x] sudo privileges not detected!!!\n"
	printf "This must be run as root.\nUse: ${NC}'sudo bash $0'\n"
 	exit
fi

unset GREP_OPTIONS

enable_camera () {
    printf "${BLUE}[i] Enabling camera...${NC}\n"
    #sudo raspi-config nonint do_camera 0
    set_config_var start_x 1 /boot/config.txt
    CUR_GPU_MEM=$(get_config_var gpu_mem /boot/config.txt)
    if [ -z "$CUR_GPU_MEM" ] || [ "$CUR_GPU_MEM" -lt 128 ]; then
      set_config_var gpu_mem 128 /boot/config.txt
    fi
    sed /boot/config.txt -i -e "s/^startx/#startx/"
    sed /boot/config.txt -i -e "s/^fixup_file/#fixup_file/"
    printf "${BLUE}[i] Camera enabled!${NC}\n"
}

install_dependencies () {
    printf "${BLUE}[i] Installing dependencies...${NC}\n"
    apt-get update
    apt-get install -fy python3 python3-pip python3-dev python3-rpi.gpio python-opencv python3-picamera python3-pil python3-numpy
    apt-get install opencv3-python
    pip3 install -r requirements.txt
    pip3 install scipy 
    enable_camera()
    printf "${BLUE}[i] Dependencies installed!${NC}\n"
    printf "${GREEN} Done!${NC}\n"
}

DIR = "/opt/hawkeye/"

if [ -d "$DIR" ]; then
    printf "${BLUE}[i] Hawkeye found in /opt/ !${NC}\n"
    cd $DIR
    install_dependencies()
else
    printf "${YELLOW}[!] Hawkeye not found in /opt/ !${NC}\n"
    printf "${BLUE}[i] Cloning Hawkeye to /opt/...${NC}\n"
    cd /opt/
    git clone https://github.com/msmcs-robotics/hawkeye.git
    printf "${GREEN} Successfully cloned hawkeye...${NC}\n"
    install_dependencies
fi