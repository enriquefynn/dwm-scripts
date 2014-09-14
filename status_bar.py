#!/usr/bin/env python

import json
import urllib2
import re
from subprocess import call,check_output

redfg = '\x1b[38;5;196m'
bluefg = '\x1b[38;5;21m'
darkgreenfg = '\x1b[38;5;78m'
darkbluefg = '\x1b[38;5;74m'
winefg = '\x1b[38;5;118m'


redbg = '\x1b[48;5;196m'
greenbg = '\x1b[48;5;47m'
yellowbg = '\x1b[48;5;226m'
blackbg = '\x1b[48;5;16m'
reset = '\x1b[0m'

#BTC
def getCoinFromBtce(coin):
    try:
        ccoin = round(json.loads(urllib2.urlopen("https://btc-e.com/api/2/{}_usd/ticker"\
                .format(coin)).read())['ticker']['last'], 2)
    except:
        return None
    return ccoin

#Weather
city_name = 'London'
def getWeatherInfo(cityName):
    w = {}
    try:
        weather = json.loads(urllib2.urlopen("http://api.openweathermap.org/data/2.5/forecast/daily?q={}&units=metric&cnt=1".format(cityName)).read())['list'][0]
        w['description'] = weather['weather'][0]['description']
        w['temp_min'] = weather['temp']['min']
        w['temp_max'] = weather['temp']['max']
    except:
        return None
    return w

weather = getWeatherInfo(city_name)
weather_bar = []
if weather != None:
    weather_bar = "{} {}{}C{}-{}{}C{} | ".format(weather['description'], bluefg, weather['temp_min'], reset, redfg, weather['temp_max'], reset)

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
    else:
        bg = redbg
    battery_bar = ['Batt: ', bg, ' '*(battery_percentage/10), \
            blackbg, ' '*(10-(battery_percentage/10)), reset, ' ', str(battery_percentage) + '%']

#Wireless
wlan = check_output(['ifconfig', 'wlan0'])
try:
    ssid = re.search(r'ssid \t*\"*(.+?)\"* channel', wlan).group(1)
except:
    ssid = None

#Date
date = [check_output('date').strip()]

attr_list = []
attr_list += weather_bar
if ssid != None:
    attr_list += ['wlan: ', winefg, ssid, reset, ' | ']

btc_ticker = getCoinFromBtce('btc')
ltc_ticker = getCoinFromBtce('ltc')
if btc_ticker != None and ltc_ticker != None:
    attr_list.extend(['{}BTC: {} {}LTC: {}{} '.format(darkgreenfg,\
            btc_ticker,\
            darkbluefg,\
            ltc_ticker,\
            reset)])
attr_list += '| '
attr_list.extend(battery_bar)
attr_list += ' | '
attr_list.extend(date)

call(['xsetroot','-name',''.join(
    attr_list
)], shell=False)
