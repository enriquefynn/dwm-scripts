#!/usr/bin/env bash
setxkbmap -layout br
xbindkeys

while true; do
    ./scripts/dwm-scripts/status_bar.py&
	sleep 15
done &

#Exec the Wallpaper changer 20m
./Wallpapers/wp_changer.sh 1200&

exec dwm
