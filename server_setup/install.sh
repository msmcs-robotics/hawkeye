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

setup_server () {
	printf "${BLUE}[i] Setting up server...${NC}\n"
	chmod 777 server_stuff/hawkeye.service
	cp server_stuff/hawkeye.service /etc/systemd/system/
	systemctl enable hawkeye.service
	systemctl start hawkeye.service
	systemctl enable hawkeye.service
	systemctl start hawkeye.service
	printf "${BLUE}[i] Server setup complete!${NC}"
	printf "${GREEN} Done!${NC}\n"
}

DIR = "/opt/hawkeye/"

if [ -d "$DIR" ]; then
	printf "${BLUE}[i] Hawkeye found in /opt/ !${NC}\n"
	cd $DIR
	setup_server()
else
	printf "${YELLOW}[!] Hawkeye not found in /opt/ !${NC}\n"
	printf "${BLUE}[i] Cloning Hawkeye to /opt/...${NC}\n"
	cd /opt/
	git clone https://github.com/msmcs-robotics/hawkeye.git
	cd $DIR
	setup_server()
fi