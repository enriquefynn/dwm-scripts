#!/usr/bin/env python

import json
import time
import urllib2
import re
from subprocess import call,check_output

redfg = '\x1b[38;5;196m'
bluefg = '\x1b[38;5;21m'
darkgreenfg = '\x1b[38;5;78m'
darkbluefg = '\x1b[38;5;74m'
winefg = '\x1b[38;5;118m'
yellowfg = '\x1b[38;5;226m'

redbg = '\x1b[48;5;196m'
greenbg = '\x1b[48;5;47m'
yellowbg = '\x1b[48;5;226m'
blackbg = '\x1b[48;5;16m'
reset = '\x1b[0m'
proxy = urllib2.ProxyHandler()
opener = urllib2.build_opener(proxy)

#BTC
def getCoinFromBtce(coin):
    try:
        ccoin = round(json.loads(opener.open("https://btc-e.com/api/2/{}_usd/ticker"\
                .format(coin)).read())['ticker']['last'], 2)
    except:
        return None
    return ccoin

#Weather
city_name = 'Lugano'
def getWeatherInfo(cityName):
    w = {}
    try:
        weather = json.loads(opener.open("http://api.openweathermap.org/data/2.5/weather?q={}&units=metric".format(cityName)).read())
        w['temp_min'] = weather['main']['temp_min']
        w['temp_act'] = weather['main']['temp']
        w['temp_max'] = weather['main']['temp_max']
        w['sunrise'] = weather['sys']['sunrise']
        w['sunset'] = weather['sys']['sunset']
    except:
        return None
    return w

weather = getWeatherInfo(city_name)
weather_bar = []
if weather != None:
    sunrise = time.strftime('%H:%M', time.localtime(weather['sunrise']))
    sunset = time.strftime('%H:%M', time.localtime(weather['sunset']))
    weather_bar = " {}{}C{}-{}{}C{}-{}{}C{} {}{}{}-{}{}{} | ".format(bluefg, weather['temp_min'], reset, 
            winefg, weather['temp_act'], reset, 
            redfg, weather['temp_max'], reset,
            yellowfg, sunrise, reset,
            redfg, sunset, reset)

#Battery
battery = check_output(['acpiconf','-i', '0'])
battery_state = re.search(r'State:\t*(\w*)', battery).group(1)
battery_percentage = int(re.search(r'Remaining capacity:\t*(\d*)', battery).group(1))
battery_bar = [bluefg, 'On AC', reset]

if battery_state != 'high':
    if battery_percentage >= 60:
        bg = greenbg
    elif 60 > battery_percentage > 30:
        bg = yellowbg
    elif battery_percentage <= 3:
        call(['shutdown', '-p', 'now'])
    else:
        bg = redbg
    battery_bar = ['Batt: ', bg, ' '*(battery_percentage/10), \
            blackbg, ' '*(10-(battery_percentage/10)), reset, ' ', str(battery_percentage) + '%']
    if battery_state == 'charging':
        battery_bar.append('c')
#Wireless
try:
    wlan = check_output(['ifconfig', 'wlan0'])
    ssid = re.search(r'ssid \t*\"*(.+?)\"* channel', wlan).group(1)
except:
    ssid = None

#Sound
sound = re.search(r'hw.snd.default_unit: (.*)', check_output(['sysctl', 'hw.snd.default_unit'])).group(1)
if sound == '0':
    sound = 'Speaker'
elif sound == '1':
    sound = 'Headset'
else:
    sound = 'HDMI'

#Date
date = [check_output(['date', '+%d/%m/%Y %H:%M']).strip()]

attr_list = []
attr_list.extend(sound)
attr_list += weather_bar
if ssid != None:
    attr_list += ['wlan: ', winefg, ssid, reset, ' | ']

btc_ticker = getCoinFromBtce('btc')
if btc_ticker != None:
    attr_list.extend(['{}BTC: {} {}'.format(darkgreenfg,\
            btc_ticker,\
            darkbluefg,\
            reset)])
attr_list += '| '
attr_list.extend(battery_bar)
attr_list += ' | '
attr_list.extend(date)

call(['xsetroot','-name',''.join(
    attr_list
)], shell=False)
