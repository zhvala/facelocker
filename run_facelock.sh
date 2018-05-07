#!/bin/sh

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	if [ -f /usr/bin/apt ]; then
		sudo /usr/bin/apt install python3 python3-pip python3-venv gnome-screensaver
	else
		echo "only support Linux distribution based on debian."
		exit 1
	fi
elif [[ "$OSTYPE" == "darwin" ]]; then
	if [ -f /usr/bin/brew ] || [ -f /usr/local/bin/brew ]; then
		brew install python3
	else
		echo "please install brew first."
		exit 1
	fi
fi

python3 -m venv venv && venv/bin/pip -r requirements.txt && nohup venv/bin/python facelocker.py &
