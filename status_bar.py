#!/usr/bin/env python
##testcoloredstatus.py

import json
import urllib2
import re
from subprocess import call,check_output


def getBTCAvgFromBtce():
    try:
        btc = round(json.loads(urllib2.urlopen("https://btc-e.com/api/2/btc_usd/ticker")\
                .read())['ticker']['last'], 2)
    except:
        return None
    return btc

def getLTCAvgFromBtce():
    try:
        ltc = round(json.loads(urllib2.urlopen("https://btc-e.com/api/2/ltc_usd/ticker")\
                .read())['ticker']['last'], 2)
    except:
        return None
    return ltc

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

battery = check_output(['acpiconf','-i', '0'])
battery_state = re.search(r'State:\t*(\w*)', battery).group(1)
battery_percentage = int(re.search(r'Remaining capacity:\t*(\d*)', battery).group(1))
battery_bar = [bluefg, 'On AC', reset]


wlan = check_output(['ifconfig', 'wlan0'])
ssid = re.search(r'ssid \t*\"(.+?)\"', wlan).group(1)

#battery_state = ''
#battery_percentage = 64

if battery_state != 'high':
    if battery_percentage >= 60:
        bg = greenbg
    elif 60 > battery_percentage > 30:
        bg = yellowbg
    else:
        bg = redbg
    battery_bar = ['Batt: ', bg, ' '*(battery_percentage/10), \
            blackbg, ' '*(10-(battery_percentage/10)), reset, ' ', str(battery_percentage) + '%']

date = [check_output('date').strip()]

attr_list = []
if ssid != None:
    attr_list = ['wlan: ', winefg, ssid, reset, ' ']

btc_ticker = getBTCAvgFromBtce()
ltc_ticker = getLTCAvgFromBtce()
if btc_ticker != None and ltc_ticker != None:
    attr_list.extend(['{}BTC: {} {}LTC: {}{} '.format(darkgreenfg,\
            getBTCAvgFromBtce(),\
            darkbluefg,\
            getLTCAvgFromBtce(),\
            reset)])
attr_list+= '| '
attr_list.extend(battery_bar)
attr_list+= ' | '
attr_list.extend(date)

call(['xsetroot','-name',''.join(
    attr_list
)], shell=False)
