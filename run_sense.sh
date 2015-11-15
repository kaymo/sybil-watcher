#!/bin/bash

cd /home/pi/sybil
python ./sense.py

if [ "$?" = "1" ]; then
  python ./sense.py
fi

