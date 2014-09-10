#!/usr/bin/env python
##testcoloredstatus.py

import json
import urllib2
from subprocess import call,check_output


def getBTCAvgFromBtce():
    return round(json.loads(urllib2.urlopen("https://btc-e.com/api/2/btc_usd/ticker")\
            .read())['ticker']['avg'], 2)
def getLTCAvgFromBtce():
    return round(json.loads(urllib2.urlopen("https://btc-e.com/api/2/ltc_usd/ticker")\
            .read())['ticker']['avg'], 2)

redfg = '\x1b[38;5;196m'
bluefg = '\x1b[38;5;21m'
darkgreenfg = '\x1b[38;5;78m'
darkbluefg = '\x1b[38;5;74m'


redbg = '\x1b[48;5;196m'
greenbg = '\x1b[48;5;47m'
yellowbg = '\x1b[48;5;226m'
blackbg = '\x1b[48;5;16m'
reset = '\x1b[0m'

battery = check_output(['acpiconf','-i', '0']).split('\n')
battery_state = battery[12][9:-1]
battery_percentage = int(battery[13][20:-1])
battery_bar = [bluefg, 'On AC', reset]

#battery_state = ''
#battery_percentage = 10

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

attr_list = ['{}BTC: {} {}LTC: {}{} '.format(darkgreenfg,\
        getBTCAvgFromBtce(),\
        darkbluefg,\
        getLTCAvgFromBtce(),\
        reset)]
attr_list.extend(battery_bar)
attr_list+= ' | '
attr_list.extend(date)

call(['xsetroot','-name',''.join(
    attr_list
)], shell=False)
