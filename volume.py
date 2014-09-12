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

mixer = check_output(['mixer', 'vol'])
volume = int(re.search(r'(\d+)', mixer).group(0))

if volume >= 60:
    bg = greenbg
elif 60 > volume > 30:
    bg = yellowbg
else:
    bg = redbg
attr_list = ['Volume: ', bg, ' '*(volume/5), \
        blackbg, ' '*(20-(volume/5)), reset, ' ', str(volume) + '%']

call(['xsetroot','-name',''.join(
    attr_list
)], shell=False)
