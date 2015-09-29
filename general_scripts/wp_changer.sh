#!/usr/bin/env zsh

while true; 
do
    for i in `ls ~/Wallpapers/*.png ~/Wallpapers/*.jpg | sort -R`
    do
        hsetroot -fill $i
        sleep $1
    done
done

