#!/bin/bash

export DISPLAY=:0
xset s off
xset -dpms 
xset s noblank
python3 /home/pi/HSI_main.py $1
