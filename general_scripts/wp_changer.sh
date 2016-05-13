#!/usr/bin/env zsh

IMG=$(ls ~/Wallpapers/*.png ~/Wallpapers/*.jpg | sort -R | tail -n 1)
hsetroot -fill $IMG
echo $IMG
