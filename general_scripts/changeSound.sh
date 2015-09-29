#!/usr/bin/env bash

nextSound=$((((`sysctl hw.snd.default_unit | cut -d ' ' -f 2` + 1))%3))
sysctl hw.snd.default_unit=$nextSound
