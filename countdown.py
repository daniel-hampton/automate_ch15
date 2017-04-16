#! python3
"""
countdown.py - a simple countdown script.
"""

import time
import subprocess
import os
import signal
import psutil


timeLeft = 30
while timeLeft > 0:
    print('\x1b[2K', end='')
    # print(' ' * 10, end='\r')  # manually clears the line. Escape character \033[K wasn't working on cmd prompt
    print(timeLeft, end='\r')
    # print('hello')
    # print(6)
    time.sleep(0.1)
    timeLeft -= 1

# At the end of the countdown timer, play a sound file.
myProcess = subprocess.Popen(['start', '/WAIT', 'alarm.txt'], shell=True)
time.sleep(5)
artichoke = psutil.Process(myProcess.pid)
for proc in artichoke.children(recursive=True):
    proc.kill()
artichoke.kill()
